from django.db import models
from django.contrib.auth import get_user_model

from .lesson import Lesson

class Test(models.Model):
    name = models.CharField('Имя теста', max_length=50, blank=True, null=False)
    test_number = models.PositiveIntegerField('Номер теста')
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        verbose_name='ID урока',
        blank=False, 
        null=False
    )
    hidden = models.BooleanField('Скрытый', null=False, blank=False, default=True)

    def get_questions(self):
        return self.questions.all()

    class Meta:
        verbose_name = 'тест'
        ordering = ('test_number', )


class TestResults(models.Model):
    test = models.ForeignKey(
        Test,
        on_delete=models.CASCADE,
        verbose_name='Тест',
        blank=False,
        null=False
    )
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        blank=False,
        null=False
    )
    start_time = models.TimeField(
        'Время начала теста',
        auto_now_add=True,
        blank=False,
        null=False
    )
    end_time = models.TimeField(
        'Время конца теста',
        blank=False,
        null=True
    )
    result = models.FloatField(
        'Результаты теста',
        blank=False,
        null=True
    )

    class Meta:
        ordering = ('-end_time', )