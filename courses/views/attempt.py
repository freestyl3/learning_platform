import json

from django.views.decorators.cache import never_cache
from django.views.generic import CreateView, DetailView
from django.http import HttpResponse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import get_user_model

from ..models import Attempt, Question, Answer, Test

@method_decorator(never_cache, name='dispatch')
class AttemptCreateView(LoginRequiredMixin, CreateView):
    ##TODO## userpassestestmixin
    model = Attempt
    fields: list[str] = []
    template_name = 'courses/test/take_test.html'

    def validate_answers(self, user_data):
        score = 0
        time_end = timezone.now().isoformat()
        data = dict()
        question_list = []

        for question in self.get_queryset():
            answers = user_data.getlist(question.text)

            question_data = dict()
            question_data['text'] = question.text
            question_data['type'] = question.type
            question_data['answers'] = [answer.answer_text for answer in question.get_answers()] if question.type != 'input' else 'Ответ: '
            question_data['user_answers'] = answers

            if question.type == 'input':
                right_answer = Answer.objects.get(question=question).answer_text
                if answers[0].lower() == right_answer.lower():
                    question_data['is_correct'] = True
                    score += 1
                else:
                    question_data['is_correct'] = False
            elif question.type == 'single':
                right_answer = Answer.objects.get(question=question, is_correct=True).answer_text
                if answers and (answers[0] == right_answer):
                    question_data['is_correct'] = True
                    score += 1
                else:
                    question_data['is_correct'] = False
            elif question.type == 'choices':
                right_answers = set([answer.answer_text for answer in Answer.objects.filter(question=question, is_correct=True)])
                if right_answers == set(answers):
                    question_data['is_correct'] = True
                    score += 1
                else:
                    question_data['is_correct'] = False
            elif question.type == 'matching':
                right_answers = list(map(str, [answer.match_pair for answer in Answer.objects.filter(question=question, is_correct=True)]))
                c = 0
                for elem1, elem2 in zip(right_answers, answers):
                    if elem1 == elem2:
                        c += 1
                score += (c / len(right_answers))
                if score == 1:
                    question_data['is_correct'] = True
                else:
                    question_data['is_correct'] = False
            question_list.append(question_data)
        
        data['questions'] = question_list
        data['time_start'] = user_data.get('time_start')
        data['time_end'] = time_end
        data['score'] = score / len(self.get_queryset()) * 100

        return data

    def get_queryset(self):
        return Question.objects.filter(test=self.kwargs.get('test_id'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        answers = {}
        for question in self.get_queryset():
            answers[question] = question.get_answers()
        context['data'] = answers
        return context
    
    def post(self, request, test_id):
        data = self.validate_answers(request.POST)
        score = data['score']

        Attempt.objects.create(
            user=self.request.user,
            test=Test.objects.get(pk=test_id),
            started_at=data['time_start'],
            ended_at=data['time_end'],
            data=data,
            score=data['score']
        )

        return HttpResponse(f'Ваш результат - {score}%<br>{json.dumps(data)}')
    
class AttemptListView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Attempt
    pk_url_kwarg = 'test_id'
    template_name = 'courses/test/attempt_list.html'

    def get_test(self):
        return Test.objects.get(pk=self.kwargs.get(self.pk_url_kwarg))

    def test_func(self):
        return self.request.user == self.get_test().lesson.module.course.author
    
    def get_queryset(self): ###TODO###
        args = Attempt.objects.filter(test=self.get_test())

        args = args.order_by('user', '-score', '-ended_at')
        args = args.distinct('user')
        args = args.order_by('user', '-score', '-ended_at')
        print(args[:1])
        # args = Attempt.objects.filter(test=self.get_test()).order_by('-score')
        # args.aggregate(Max('score'))
        return args
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['attempts'] = self.get_queryset()
        context['test'] = self.get_test()
        return context
        
