from django.db import models

# Create your models here.

class Test(models.Model):
    name = models.CharField('Имя теста', max_length=50)
    
class QuestionTypes(models.Model):
    type = models.CharField('Тип теста', max_length=20)

class Questions(models.Model):
    text = models.CharField('Текст вопроса', max_length=50)
    choices = models
    test_id = models.ForeignKey(
        Test,
        on_delete=models.CASCADE,
        verbose_name='ID теста',
        blank=False, 
        null=False
    )
    type = models.ForeignKey(
        QuestionTypes,
        on_delete=models.CASCADE,
        verbose_name='Тип теста',
        blank=False, 
        null=False
    )
    #Правильный ответ

class Subject(models.Model):
    name = models.CharField('Название предмета', max_length=50, blank=False, null=False)

class Theory(models.Model):
    pass

class Lesson(models.Model):
    icon = models.ImageField('Картинка урока')
    lesson_number = models.IntegerField('Номер урока')
    name = models.CharField('Название', max_length=50)
    theory_id = models.ForeignKey(
        Theory, 
        on_delete=models.CASCADE,
        verbose_name='ID Теории',
        blank=False, 
        null=False
    )
    test_id = models.OneToOneField(
        Test,
        on_delete=models.CASCADE,
        verbose_name='ID теста',
        blank=False, 
        null=False
    )
    subject_id = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        verbose_name='ID предмета',
        blank=False, 
        null=False
    )
    hidden = models.BooleanField('Скрытый', blank=False, null=False, default=False)
