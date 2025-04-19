from django import forms

from .models import (Lesson, Paragraph, Test, Question, 
                     InputQuestion, ChoiceQuestion, 
                     MatchQuestion, MatchLeft, MatchRight, Course,
                     LessonImage)

class ParagraphForm(forms.ModelForm):
    class Meta:
        model = Paragraph
        fields = ('lesson', 'text', 'order')
        labels = {
            'lesson': 'Урок',
            'text': 'Текст параграфа',
            'order': 'Порядок'
        }

class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ('lesson', 'name')
        labels = {
            'lesson': 'Урок',
            'name': 'Название теста'
        }

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('test_id', 'text', 'type')

class InputQuestionForm(forms.ModelForm):
    class Meta:
        model = InputQuestion
        fields = ('question_id', 'right_answer')

class ChoiceQuestionForm(forms.ModelForm):
    class Meta:
        model = ChoiceQuestion
        fields = ('question_id', 'text', 'is_correct') 

class MatchLeftForm(forms.ModelForm):
    class Meta:
        model = MatchLeft
        fields = ('text', )

class MatchRightForm(forms.ModelForm):
    class Meta:
        model = MatchRight
        fields = ('text', )

class MatchQuestionForm(forms.ModelForm):
    class Meta:
        model = MatchQuestion
        fields = ('question_id', 'left_id', 'right_id')

class CourseCreateForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

class LessonImageForm(forms.ModelForm):
    class Meta:
        model = LessonImage
        fields = ['image', 'caption', 'order']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'caption': forms.TextInput(attrs={'class': 'form-control'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'})
        }
        labels = {
            'image': 'Изображение',
            'caption': 'Подпись',
            'order': 'Порядок отображения'
        }

class LessonForm(forms.ModelForm):
    images = forms.FileField(
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control',
            'multiple': True,
            'accept': 'image/*'
        }),
        required=False,
        label='Добавить изображения'
    )

    class Meta:
        model = Lesson
        fields = ['name', 'content', 'images']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
        }
        labels = {
            'name': 'Название урока',
            'content': 'Содержание урока',
        }
