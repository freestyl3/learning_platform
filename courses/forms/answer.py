from django import forms

from ..models import Answer, Question

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['answer_text', 'is_correct', 'match_pair']

AnswerFormSet = forms.inlineformset_factory(
    Question, 
    Answer, 
    form=AnswerForm, 
    extra=1,  # Количество пустых форм, которые нужно отобразить
    can_delete=True
)