from django import forms 

from ..models import Question


class QuestionForm(forms.ModelForm):
    type = forms.ChoiceField(
        widget=forms.Select(
            {'onchange': 'showQuestionTypeFields()'}
        ), 
        choices=[
            ('input', 'Ввод текста'), 
            ('choices', 'Выбор ответа'),
            ('matching', 'Соответствие')
        ],
        label='Тип вопроса'
    )
    class Meta:
        model = Question
        fields = ['text', 'type']
        # widgets = {
        #     'type': forms.ModelChoiceField(widget=forms.Select(
        #         {'onchange': 'showQuestionTypeFields()'}
        #         ), queryset=Question.objects.all())
        # }

# class ChoiceForm(forms.ModelForm):
#     class Meta:
#         model = ChoiceQuestion
#         fields = ['text', 'is_correct']
#         widgets = {
#             'is_correct': forms.CheckboxSelectMultiple()
#         }

# class InputForm(forms.ModelForm):
#     class Meta:
#         model = InputQuestion
#         fields = ['right_answer', ]

# class MatchiForm(forms.ModelForm):
#     class Meta:
#         model = MatchQuestion
#         fields = ['left', 'right']