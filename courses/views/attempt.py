import json

from django.views.decorators.cache import never_cache
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy

from ..models import Attempt, Question, Answer, Test

@method_decorator(never_cache, name='dispatch')
class TakeTestView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Attempt
    fields: list[str] = []
    template_name = 'courses/test/take_test.html'
    pk_url_kwarg = 'test_id'

    def post(self, request, test_id):
        if not self.request.session.get('attempt_id'):
            attempt = Attempt(
                user=self.request.user, 
                test=Test.objects.get(pk=test_id)
            )
            attempt.save()
            self.request.session['attempt_id'] = attempt.id
        else:
            attempt = self.request.session.get('attempt_id')
        context = self.get_context_data()
        return render(request, self.template_name, context=context)
        

    def test_func(self):
        return self.request.user != Test.objects.get(pk=self.kwargs.get('test_id')).lesson.module.course.author

    def get_queryset(self):
        return Question.objects.filter(test=self.kwargs.get(self.pk_url_kwarg))

    def get_context_data(self):
        context = dict()
        answers = {}
        for question in self.get_queryset():
            answers[question] = question.get_answers()
        context['data'] = answers
        context['test'] = get_object_or_404(Test, pk=self.kwargs.get('test_id'))
        return context


@method_decorator(never_cache, name='dispatch')
class AttemptUpdateView(LoginRequiredMixin, UpdateView):
    model = Attempt
    fields: list[str] = []
    template_name = 'courses/test/take_test.html'
    pk_url_kwarg = 'test_id'

    def validate_answers(self, user_data):
        score = 0
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
        attempt = Attempt.objects.get(pk=request.session.pop('attempt_id', None))

        data = self.validate_answers(request.POST)
        attempt.data = data
        attempt.score = data['score']

        attempt.save()

        return HttpResponse(f'Ваш результат - {data['score']}%')
    
class AttemptListView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Attempt
    pk_url_kwarg = 'test_id'
    template_name = 'courses/attempt/attempt_list.html'

    def get_test(self):
        return Test.objects.get(pk=self.kwargs.get(self.pk_url_kwarg))

    def test_func(self):
        return self.request.user == self.get_test().lesson.module.course.author
    
    def get_queryset(self):
        args = Attempt.objects.filter(test=self.get_test())

        args = args.order_by('user', '-score', '-ended_at')
        args = args.distinct('user')
        args = args.order_by('user', '-score', '-ended_at')
        return args
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['attempt_list'] = self.get_queryset()
        context['author'] = True
        context['test'] = self.get_test()
        return context
        

class UserAttemptsListView(LoginRequiredMixin, ListView):
    model = Attempt
    template_name = 'courses/attempt/attempt_list.html'
    pk_url_kwarg = 'test_id'
    
    def get_queryset(self):
        return Attempt.objects.filter(user=self.request.user, test=self.kwargs.get(self.pk_url_kwarg))