from django.db import models
from django.contrib.auth import get_user_model

from .test import Test

class Attempt(models.Model):
    user = models.ForeignKey(
        get_user_model(), 
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        null=False, 
        blank=False
    )
    test = models.ForeignKey(
        Test, 
        verbose_name='Тест',
        on_delete=models.CASCADE,
        null=False, 
        blank=False
    )
    started_at = models.DateTimeField(
        verbose_name='Начало',
        blank=False, 
        null=False
    )
    ended_at = models.DateTimeField(
        verbose_name='Конец',
        blank=False, 
        null=True
    )
    data = models.TextField(
        verbose_name='Данные ответов',
        blank=False,
        null=True
    )
    score = models.PositiveIntegerField(
        verbose_name='Баллы',
        blank=False,
        null=False,
        default=0
    )