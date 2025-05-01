from django import forms 

from ..models import Question


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'type']
        widgets = {
            'type': forms.RadioSelect(attrs={'onchange': 'showQuestionTypeFields()', 'class': 'type-radio'})
        }

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