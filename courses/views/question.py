from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy

from ..models import Question, Test, Answer
from ..forms import QuestionForm
from ..mixins import BaseDeleteMixin

class QuestionCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Question
    template_name = 'courses/question/question_update_test.html'
    form_class = QuestionForm

    def test_func(self):
        author = Test.objects.get(pk=self.kwargs.get('test_id')).lesson.module.course.author
        return self.request.user == author
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем начальные формы для JS
        context['js_choices'] = 0
        context['js_matches'] = 0
        return context

    def form_valid(self, form):
        # choices = [choice for choice in self.request.POST if choice.startswith('choice_text') or choice.startswith('is_correct')]
        # matches = [match for match in self.request.POST if match.startswith('match_left') or match.startswith('match_right')]
        print(self.request.POST)
        choices, matches = dict(), dict()
        for item in self.request.POST:
            print(item, f'choice_item_{item.split('_')}')
            # if item.startswith('is_correct') and f'choice_item_{item.split('_')[2]}' in self.request.POST:
            #     choices[f'choice_item_{item.split('_')[2]}'] = self.request.POST.get(item)
            # else:
            #     return self.form_invalid(form)
        print(choices, matches)
        q_type = form.cleaned_data['type']
        test = Test.objects.get(pk=self.kwargs.get('test_id'))

        question = Question.objects.create(
            test=test,
            text=self.request.POST.get('text'),
            type=q_type
        )
        
        # Обработка Input вопроса
        if q_type == 'input':
            Answer.objects.create(
                question=question,
                answer_text=self.request.POST.get('right_answer'),
                is_correct=True
            )
        
        # Обработка Choice вопроса
        elif q_type == 'choices':
            i = 0
            while f'choice_text_{i}' in self.request.POST:
                Answer.objects.create(
                    question=question,
                    answer_text=self.request.POST.get(f'choice_text_{i}'),
                    is_correct=bool(self.request.POST.get(f'is_correct_{i}'))
                )
                i += 1
        
        # Обработка Matching вопроса (с учётом опечатки)
        elif q_type == 'matching':
            i = 0
            while f'match_left_{i}' in self.request.POST:
                Answer.objects.create(
                    question=question,
                    answer_text=self.request.POST.get(f'match_left_{i}'),
                    match_pair=self.request.POST.get(f'match_right_{i}'),
                    is_correct=True
                )
                i += 1
        
        return redirect('courses:test_detail', test_id=test.pk)
    
class QuestionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Question
    template_name = 'courses/question/question_update_test.html'
    form_class = QuestionForm
    pk_url_kwarg = 'question_id'

    def test_func(self):
        return self.request.user == self.get_object().test.lesson.module.course.author
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем начальные формы для JS
        answers = self.get_object().get_answers()
        answers_count = answers.count()
        q_type = self.get_object().type
        
        choices_count = int(q_type == 'choices') * answers_count
        matches_count = int(q_type == 'matching') * answers_count
        context['answers'] = answers
        context['js_choices'] = choices_count
        context['js_matches'] = matches_count
        return context
    
    def form_valid(self, form):
        q_type = form.cleaned_data['type']
        test = self.get_object().test
        question = Question.objects.filter(
            pk=self.get_object().pk
        )

        instance_q_type = self.get_object().type

        question.update(
            text=self.request.POST.get('text'),
            type=q_type
        )
        answers = self.get_object().get_answers()

        if q_type != instance_q_type:
            Question.objects.filter(
                pk=self.get_object().pk
            ).update(
                type=q_type
            )
            for answer in answers:
                answer.delete()
                answers = []
        if q_type == 'input':
            if answers:
                for answer in answers:
                    Answer.objects.filter(
                        pk=answer.pk,
                    ).update(
                        answer_text=self.request.POST.get('right_answer')
                    )
            else:
                Answer.objects.create(
                    question=self.get_object(),
                    answer_text=self.request.POST.get('right_answer'),
                    is_correct=True
                )
        elif q_type == 'choices':
            i = 0
            end = False
            while not end:
                if answers:
                    for answer in answers:
                        Answer.objects.filter(
                            pk=answer.pk
                        ).update(
                            answer_text=self.request.POST.get(f'choice_text_{i}'),
                            is_correct=bool(self.request.POST.get(f'is_correct_{i}'))
                        )
                        i += 1
                    answers = []
                if f'choice_text_{i}' in self.request.POST:
                    Answer.objects.create(
                        question=self.get_object(),
                        answer_text=self.request.POST.get(f'choice_text_{i}'),
                        is_correct=bool(self.request.POST.get(f'is_correct_{i}'))
                    )
                    i += 1
                else:
                    end = True
        
        elif q_type == 'matching':
            i = 0
            end = False
            while not end:
                if answers:
                    for answer in answers:
                        Answer.objects.filter(
                            pk=answer.pk
                        ).update(
                            answer_text=self.request.POST.get(f'match_left_{i}'),
                            match_pair=self.request.POST.get(f'match_right_{i}')
                        )
                        i += 1
                    answers = []
                if f'match_left_{i}' in self.request.POST:
                    Answer.objects.create(
                        question=self.get_object(),
                        answer_text=self.request.POST.get(f'match_left_{i}'),
                        match_pair=self.request.POST.get(f'match_right_{i}'),
                        is_correct=True
                    )
                    i += 1
                else:
                    end = True
            while f'match_left_{i}' in self.request.POST:
                Answer.objects.update_or_create(
                    question=question,
                    answer_text=self.request.POST.get(f'match_left_{i}'),
                    match_pair=self.request.POST.get(f'match_right_{i}'),
                    is_correct=True
                )
                i += 1
        
        return redirect('courses:test_detail', test_id=test.pk)
    
    

class QuestionDeleteView(LoginRequiredMixin, UserPassesTestMixin, BaseDeleteMixin):
    model = Question
    template_name = 'courses/delete_form.html'
    pk_url_kwarg = 'question_id'

    def test_func(self):
        return self.request.user == self.get_object().test.lesson.module.course.author
    
    def get_delete_name(self):
        return self.get_object().text
    
    def get_success_url(self):
        kwargs = {'test_id': self.get_object().test.pk}
        return reverse_lazy('courses:test_detail', kwargs=kwargs)
    
