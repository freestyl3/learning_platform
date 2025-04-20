from django.db import models
from users.models import MyUser
from django.contrib.auth.models import User

# Create your models here.

class Test(models.Model):
    name = models.CharField('Имя теста', max_length=50, blank=True, null=False)
    lesson = models.OneToOneField(
        'Lesson',
        on_delete=models.CASCADE,
        verbose_name='Урок',
        blank=False, 
        null=False
    )
    
    def __str__(self):
        return f"Тест: {self.name} ({self.lesson.name})"

class QuestionType(models.TextChoices):
    INPUT = 'input', 'Ввод текста'
    MULTIPLE_CHOICE = 'multiple_choice', 'Множественный выбор'

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
        default=QuestionType.INPUT,
        blank=False,
        null=False
    )
    
    def __str__(self):
        return f"Вопрос: {self.text}"

class InputQuestion(models.Model):
    right_answer = models.CharField(
        'Правильный ответ',
        max_length=50,
        blank=False,
        null=False
    )
    question_id = models.OneToOneField(
        Question,
        verbose_name='ID вопроса',
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name='inputquestion'
    )

class ChoiceQuestion(models.Model):
    text = models.CharField('Текст варианта ответа', max_length=50, blank=False, null=False)
    is_correct = models.BooleanField('Правильный ответ', default=False, blank=False, null=False)
    question_id = models.ForeignKey(
        Question,
        verbose_name='ID вопроса',
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name='choicequestion_set'
    )

class MatchLeft(models.Model):
    text = models.CharField('Текст варианта ответа', max_length=50, blank=False, null=False)

class MatchRight(models.Model):
    text = models.CharField('Текст варианта ответа', max_length=50, blank=False, null=False)

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
    right_id = models.ForeignKey(
        MatchRight,
        verbose_name='ID правого варианта ответа',
        on_delete=models.CASCADE,
        blank=False,
        null=False
    )

class Lesson(models.Model):
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    content = models.TextField(verbose_name='Содержание урока')
    lesson_number = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['lesson_number']

    def __str__(self):
        return f"{self.course.name} - Урок {self.lesson_number}: {self.name}"

class Paragraph(models.Model):
    text = models.TextField('Текст параграфа', max_length=500, blank=False, null=False)
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE, 
        verbose_name='Урок',
        blank=True,
        null=False
    )
    order = models.IntegerField('Порядок параграфов')

    def __str__(self):
        return f"Параграф {self.order} урока {self.lesson.name}"

class Course(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    teacher = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class LessonImage(models.Model):
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Урок'
    )
    image = models.ImageField(
        upload_to='lesson_images/%Y/%m/%d/',
        verbose_name='Изображение'
    )
    caption = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Подпись к изображению'
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='Порядок отображения'
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['order', 'created_at']
        verbose_name = 'Изображение урока'
        verbose_name_plural = 'Изображения урока'

    def __str__(self):
        return f"Изображение {self.order} для урока {self.lesson.name}"

class TestResult(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    score = models.FloatField()  # Процент правильных ответов
    completed_at = models.DateTimeField()
    
    class Meta:
        unique_together = ['user', 'test']  # Один пользователь может пройти тест только один раз
        ordering = ['-completed_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.test.name} ({self.score}%)"
