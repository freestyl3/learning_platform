from django.db import models
from django.contrib.auth import get_user_model

class Course(models.Model):
    name = models.CharField('Название курса', max_length=50, blank=False, null=False)
    description = models.TextField('Описание курса', blank=False, null=False)
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        verbose_name='ID Автора',
        blank=False,
        null=False
    )
    users = models.ManyToManyField(
        get_user_model(), 
        related_name='users', 
        through='UsersCourses'
    )
    rating = models.IntegerField(
        'Рейтинг курса', 
        blank=False, 
        null=False, 
        default=0
    )

    class Meta:
        verbose_name = 'курс'


class UsersCourses(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        verbose_name='ID пользователя',
        blank=False,
        null=False
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name='ID курса',
        blank=False,
        null=False
    )
