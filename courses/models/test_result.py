from django.db import models

from .attempt import Attempt

class TestResult(models.Model):
    attempt = models.ForeignKey(
        Attempt,
        verbose_name='Попытка',
        on_delete=models.CASCADE,
        blank=False,
        null=False
    )
    