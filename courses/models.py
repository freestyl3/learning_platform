from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

# class Test(models.Model):
#     name = models.CharField('Имя теста', max_length=50, blank=True, null=False)
#     test_number = models.PositiveIntegerField('Номер теста')
#     lesson_id = models.ForeignKey(
#         'Lesson',
#         on_delete=models.CASCADE,
#         verbose_name='ID урока',
#         blank=False, 
#         null=False
#     )
#     hidden = models.BooleanField('Скрытый', null=False, blank=False, default=True)

#     class Meta:
#         verbose_name = 'тест'
#         ordering = ('test_number', )
    
class QuestionType(models.TextChoices):
    INPUT = 'input'
    SINGLE_CHOICE = 'single_choices'
    MULTIPLE_CHOICE = 'multiple_choice'
    MATCHING = 'mathcing'

class Question(models.Model):
    text = models.CharField('Текст вопроса', max_length=50, blank=True, null=False)
    test_id = models.ForeignKey(
        Test,
        on_delete=models.CASCADE,
        verbose_name='ID теста',
        blank=False, 
        null=False
    )
    type = models.CharField(
        'Тип вопроса',
        max_length=15,
        choices=QuestionType.choices,
        blank=False,
        null=False
    )

class InputQuestion(models.Model):
    right_answer = models.CharField(
        'Правильный ответ',
        max_length=50,
        blank=False,
        null=False
    )
    question_id = models.ForeignKey(
        Question,
        verbose_name='ID вопроса',
        on_delete=models.CASCADE,
        blank=False,
        null=False
    )

class ChoiceQuestion(models.Model):
    text = models.CharField('Текст варианта ответа', max_length=50, blank=False, null=False)
    is_correct = models.BooleanField('Правильный ответ', default=False, blank=False, null=False)
    question_id = models.ForeignKey(
        Question,
        verbose_name='ID вопроса',
        on_delete=models.CASCADE,
        blank=False,
        null=False
    )

class MatchQuestion(models.Model):
    question_id = models.ForeignKey(
        Question,
        verbose_name='ID вопроса',
        on_delete=models.CASCADE,
        blank=False,
        null=False
    )
    left = models.CharField('Текст левого варианта ответа', max_length=50, blank=False, null=False)
    right = models.CharField('Текст правого варианта ответа', max_length=50, blank=False, null=False)

# class Course(models.Model):
#     name = models.CharField('Название предмета', max_length=50, blank=False, null=False)
#     description = models.CharField('Описание предмета', max_length=200, blank=False, null=False)
#     author = models.ForeignKey(
#         get_user_model(),
#         on_delete=models.CASCADE,
#         verbose_name='ID Автора',
#         blank=False,
#         null=False
#     )
#     users = models.ManyToManyField(
#         get_user_model(), 
#         related_name='users', 
#         through='UsersCourses'
#     )

#     class Meta:
#         verbose_name = 'курс'
    

# class Lesson(models.Model):
#     lesson_number = models.PositiveIntegerField('Номер урока')
#     name = models.CharField('Название', max_length=50)
#     content = models.TextField('Содержание урока', blank=True, null=False)
#     course_id = models.ForeignKey(
#         Course,
#         on_delete=models.CASCADE,
#         verbose_name='ID предмета',
#         blank=False, 
#         null=False
#     )
#     hidden = models.BooleanField('Скрытый', blank=False, null=False, default=False)

#     class Meta:
#         verbose_name = 'урок'
#         ordering = ('lesson_number', )


# class UsersCourses(models.Model):
#     user_id = models.ForeignKey(
#         get_user_model(),
#         on_delete=models.CASCADE,
#         verbose_name='ID пользователя',
#         blank=False,
#         null=False
#     )
#     course_id = models.ForeignKey(
#         Course,
#         on_delete=models.CASCADE,
#         verbose_name='ID курса',
#         blank=False,
#         null=False
#     )
