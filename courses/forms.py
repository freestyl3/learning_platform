from django.forms import ModelForm
from . import models

class CreateCourseForm(ModelForm):
    class Meta:
        model = models.Course
        fields = ('name', 'description',)
