from django.db import models 

from .question import Question

class Answer(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        verbose_name='Вопрос',
        blank=False,
        null=False,
        related_name='answers'
    )
    answer_text = models.CharField(
        'Текст ответа',
        max_length=128,
        blank=False,
        null=False
    )
    is_correct = models.BooleanField(
        'Правильный',
        blank=False,
        null=False,
        default=False
    )
    match_pair = models.CharField(
        'Пара к ответу',
        max_length=128,
        blank=False,
        null=True,
        default=None
    )