from django import forms

from ..models import Lesson

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ('name', 'content', 'hidden')
        widgets = {
            'content': forms.Textarea()
        }