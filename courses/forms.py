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
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'type']
        widgets = {
            'text': forms.TextInput(attrs={
                'class': 'form-field__input',
                'placeholder': 'Введите текст вопроса'
            }),
            'type': forms.Select(attrs={
                'class': 'form-field__input',
            }),
        }

class InputQuestionForm(forms.ModelForm):
    class Meta:
        model = InputQuestion
        fields = ['right_answer']
        widgets = {
            'right_answer': forms.TextInput(attrs={
                'class': 'form-field__input',
                'placeholder': 'Введите правильный ответ'
            }),
        }

class ChoiceQuestionForm(forms.ModelForm):
    class Meta:
        model = ChoiceQuestion
        fields = ['text', 'is_correct']
        widgets = {
            'text': forms.TextInput(attrs={
                'class': 'form-field__input',
                'placeholder': 'Введите вариант ответа'
            }),
            'is_correct': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }

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
    class Meta:
        model = Lesson
        fields = ['name', 'content']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
        }
        labels = {
            'name': 'Название урока',
            'content': 'Содержание урока',
        }
