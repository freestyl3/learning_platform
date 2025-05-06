from django.db import models

from .test import Test

class Question(models.Model):

    class QuestionType(models.TextChoices):
        INPUT = 'input'
        CHOICES = 'choices'
        MATCHING = 'matching'
        
    text = models.CharField('Текст вопроса', max_length=50, blank=False, null=False)
    test= models.ForeignKey(
        Test,
        on_delete=models.CASCADE,
        verbose_name='ID теста',
        blank=False, 
        null=False,
        related_name='questions'
    )
    type = models.CharField(
        'Тип вопроса',
        max_length=15,
        choices=QuestionType.choices,
        blank=False,
        null=False
    )

    def get_answers(self):
        return self.answers.all()

# class InputQuestion(models.Model):
#     right_answer = models.CharField(
#         'Правильный ответ',
#         max_length=50,
#         blank=False,
#         null=False
#     )
#     question = models.ForeignKey(
#         Question,
#         verbose_name='ID вопроса',
#         on_delete=models.CASCADE,
#         blank=False,
#         null=False
#     )

# class ChoiceQuestion(models.Model):
#     text = models.CharField('Текст варианта ответа', max_length=50, blank=False, null=False)
#     is_correct = models.BooleanField('Правильный ответ', default=False, blank=False, null=False)
#     question = models.ForeignKey(
#         Question,
#         verbose_name='ID вопроса',
#         on_delete=models.CASCADE,
#         blank=False,
#         null=False
#     )

# class MatchQuestion(models.Model):
#     question = models.ForeignKey(
#         Question,
#         verbose_name='ID вопроса',
#         on_delete=models.CASCADE,
#         blank=False,
#         null=False
#     )
#     left = models.CharField('Текст левого варианта ответа', max_length=50, blank=False, null=False)
#     right = models.CharField('Текст правого варианта ответа', max_length=50, blank=False, null=False)