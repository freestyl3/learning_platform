from django import forms

from .models import (Subject, Lesson, Paragraph, Test, Question, 
                     InputQuestion, ChoiceQuestion, 
                     MatchQuestion, MatchLeft, MatchRight)

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ('name', )

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ('icon', 'subject_id', 'lesson_number', 'hidden')
        widgets = {
            'icon': forms.FileInput(attrs={'type': 'image'})
        }

class ParagraphForm(forms.ModelForm):
    class Meta:
        model = Paragraph
        fields = ('lesson_id', 'text', 'order')

class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ('lesson_id', 'name')

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
