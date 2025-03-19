from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class MyUser(AbstractUser):
    is_teacher = models.BooleanField("Преподаватель", blank=False, null=False)
