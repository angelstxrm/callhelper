from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

class Organisation(models.Model):
    name = models.CharField('Название', max_length=100)
    director = models.ForeignKey(
        User, models.RESTRICT, related_name='organisations_directors',
        verbose_name='Директор',
    )
    employees = models.ManyToManyField(
        User, related_name='organisations_employees', verbose_name='Сотрудники', blank=True,
    )

    class Meta:
        verbose_name = 'Организацию'
        verbose_name_plural = 'Организации'
        ordering = ['name']

    def __str__(self):
        return f'{self.name} ({self.pk})'

