from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy

from ..models import Question, Test, Answer
from ..forms import QuestionForm
from ..mixins import BaseDeleteMixin

class QuestionCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Question
    template_name = 'courses/question/question_create_test.html'
    fields = ['text', 'type']

    def test_func(self):
        author = Test.objects.get(pk=self.kwargs.get('test_id')).lesson.module.course.author
        return self.request.user == author
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем начальные формы для JS
        context['initial_choices'] = range(1)
        context['initial_matches'] = range(1)
        return context

    def form_valid(self, form):
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

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['type'].widget.attrs.update({'onchange': 'showQuestionTypeFields()'})
        return form
    
class QuestionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Question
    template_name = 'courses/question/question_create_test.html'
    fields = ['text', 'type']
    pk_url_kwarg = 'question_id'

    def test_func(self):
        return self.request.user == self.get_object().test.lesson.module.course.author
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем начальные формы для JS
        choices_count = self.get_object().get_answers().count()
        context['initial_choices'] = range(1, choices_count)
        context['initial_matches'] = range(1, choices_count)
        return context
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['type'].widget.attrs.update({'onchange': 'showQuestionTypeFields()'})
        return form
    
    def form_valid(self, form):
        q_type = form.cleaned_data['type']
        test = self.get_object().test
        question = Question.objects.filter(
            pk=self.kwargs.get('question_id')
        )

        instance_q_type = self.get_object().type

        question.update(
            text=self.request.POST.get('text'),
            type=q_type
        )

        if q_type != instance_q_type:
            answers = self.get_object().get_answers()

            for answer in answers:
                answer.delete()

        else:
            ''' FIX THIS '''
            if q_type == 'input':
                # answer = Answer.objects.filter(
                #     question=self.get_object()
                # )
                for answer in self.get_object().get_answers():
                    answer.delete()
                Answer.objects.create(
                    question=self.get_object(),
                    answer_text=self.request.POST.get('right_answer'),
                    is_correct=True
                )
                # answer.update_or_create(
                #     question=self.get_object(),
                #     answer_text=self.request.POST.get('right_answer'),
                #     is_correct=True
                # )
            
            # Обработка Choice вопроса
            elif q_type == 'choices':
                i = 0
                while f'choice_text_{i}' in self.request.POST:
                    Answer.objects.update_or_create(
                        question=question,
                        answer_text=self.request.POST.get(f'choice_text_{i}'),
                        is_correct=bool(self.request.POST.get(f'is_correct_{i}'))
                    )
                    i += 1
            
            # Обработка Matching вопроса (с учётом опечатки)
            elif q_type == 'matching':
                i = 0
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
    
