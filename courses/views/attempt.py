import json

from django.views.generic import CreateView
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils import timezone

from ..models import Attempt, Question, Answer

class AttemptCreateView(CreateView):
    model = Attempt
    fields: list[str] = []
    template_name = 'courses/test/take_test.html'

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
        print(request.POST)
        score = 0
        for question in self.get_queryset():
            answers = request.POST.getlist(question.text)
            if question.type == 'input':
                right_answer = Answer.objects.get(question=question).answer_text
                if answers[0].lower() == right_answer.lower():
                    score += 1
                # print(f'{question.text} - {answers[0]} - {answers[0].lower() == right_answer}')
            elif question.type == 'choices':
                right_answers = set([answer.answer_text for answer in Answer.objects.filter(question=question, is_correct=True)])
                if right_answers == set(answers):
                    score += 1
                # print(f'{right_answers} - {set(answers)} - {right_answers == set(answers)}')
            elif question.type == 'matching':
                right_answers = list(map(str, [answer.id for answer in Answer.objects.filter(question=question, is_correct=True)]))
                # print(f'{right_answers} - {answers}')
                c = 0
                for elem1, elem2 in zip(right_answers, answers):
                    if elem1 == elem2:
                        c += 1
                        # print(f'{elem1} - {elem2}')
                score += (c / len(right_answers))
        # return redirect('courses:test_detail', test_id=test_id)
        return HttpResponse(f'Time start - {request.POST.get('time_start')}<br>Time end - {timezone.now()}<br>Ваш результат - {score / len(self.get_queryset()) * 100}%<br>{json.dumps({k: request.POST.getlist(k) for k in request.POST.keys()})}')