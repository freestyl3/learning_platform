from django.core.management.base import BaseCommand
from courses.models import Question, ChoiceQuestion, InputQuestion

class Command(BaseCommand):
    help = 'Очистка некорректных данных в базе данных'

    def handle(self, *args, **options):
        # Получаем все существующие ID вопросов
        valid_question_ids = set(Question.objects.values_list('id', flat=True))
        
        # Очищаем варианты ответов с некорректными ссылками
        invalid_choices = ChoiceQuestion.objects.exclude(question_id__in=valid_question_ids)
        invalid_choices_count = invalid_choices.count()
        invalid_choices.delete()
        
        # Очищаем текстовые ответы с некорректными ссылками
        invalid_inputs = InputQuestion.objects.exclude(question_id__in=valid_question_ids)
        invalid_inputs_count = invalid_inputs.count()
        invalid_inputs.delete()
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Удалено {invalid_choices_count} некорректных вариантов ответов и '
                f'{invalid_inputs_count} некорректных текстовых ответов'
            )
        ) 