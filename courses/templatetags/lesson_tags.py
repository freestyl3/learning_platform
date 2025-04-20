from django import template
import re
from django.utils.safestring import mark_safe
from courses.models import LessonImage

register = template.Library()

@register.filter(name='process_lesson_content')
def process_lesson_content(content, lesson):
    """
    Заменяет плейсхолдеры [IMAGE:image-X] на HTML-код изображений
    """
    def replace_image(match):
        image_id = match.group(1)
        try:
            # Получаем порядковый номер изображения из ID
            index = int(image_id.split('-')[1])
            # Получаем изображение по порядковому номеру
            image = lesson.images.all()[index]
            # Формируем HTML для изображения
            return f'<div class="lesson-image"><img src="{image.image.url}" alt="{image.caption or "Изображение урока"}" class="img-fluid"><div class="image-caption">{image.caption}</div></div>'
        except (IndexError, ValueError):
            return ''

    # Заменяем все плейсхолдеры на HTML-код изображений
    processed_content = re.sub(r'\[IMAGE:(image-\d+)\]', replace_image, content)
    return mark_safe(processed_content) 