from django import forms
from . import models

class CourseForm(forms.ModelForm):
    class Meta:
        model = models.Course
        fields = ('name', 'description',)


class LessonForm(forms.ModelForm):
    class Meta:
        model = models.Lesson
        fields = ('name', 'content', 'lesson_number', 'hidden')
        widgets = {
            'content': forms.Textarea()
        }
