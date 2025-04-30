from django.db import models
from .module import Module

class Lesson(models.Model):
    lesson_number = models.PositiveIntegerField('Номер урока')
    name = models.CharField('Название', max_length=50)
    content = models.TextField('Содержание урока', blank=True, null=False)
    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        verbose_name='ID предмета',
        blank=False, 
        null=False
    )
    hidden = models.BooleanField('Скрытый', blank=False, null=False, default=False)

    class Meta:
        verbose_name = 'урок'
        ordering = ('lesson_number', )