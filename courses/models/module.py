from django.db import models
from . import Course

class Module(models.Model):
    module_number = models.PositiveIntegerField(
        'Номер урока', 
        blank=False, 
        null=False
    )
    name = models.CharField('Название', max_length=50)
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name='Курс',
        blank=False, 
        null=False
    )
    hidden = models.BooleanField(
        'Скрытый', 
        blank=False, 
        null=False, 
        default=False
    )

    class Meta:
        verbose_name = 'модуль'
        ordering = ('module_number', )