from django.db import models
from users.models import MyUser

# Create your models here.

class Test(models.Model):
    name = models.CharField('Имя теста', max_length=50, blank=True, null=False)
    
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

class MatchLeft(models.Model):
    text = models.CharField('Текст варианта ответа', max_length=50, blank=False, null=False)

class MatchRight(MatchLeft):
    pass

class MatchQuestion(models.Model):
    question_id = models.ForeignKey(
        Question,
        verbose_name='ID вопроса',
        on_delete=models.CASCADE,
        blank=False,
        null=False
    )
    left_id = models.ForeignKey(
        MatchLeft,
        verbose_name='ID левого варианта ответа',
        on_delete=models.CASCADE,
        blank=False,
        null=False
    )
    left_id = models.ForeignKey(
        MatchRight,
        verbose_name='ID правого варианта ответа',
        on_delete=models.CASCADE,
        blank=False,
        null=False
    )

class Subject(models.Model):
    name = models.CharField('Название предмета', max_length=50, blank=False, null=False)
    users = models.ManyToManyField(MyUser)

class Theory(models.Model):
    pass

class Paragraph(models.Model):
    text = models.TextField('Текст параграфа', max_length=500, blank=False, null=False)
    theory_id = models.ForeignKey(
        Theory,
        on_delete=models.CASCADE, 
        verbose_name='ID теории',
        blank=True,
        null=False
    )
    

class Lesson(models.Model):
    icon = models.ImageField('Картинка урока')
    lesson_number = models.IntegerField('Номер урока')
    name = models.CharField('Название', max_length=50)
    theory_id = models.OneToOneField(
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
