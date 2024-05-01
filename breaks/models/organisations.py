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



class Group(models.Model):
    organisation = models.ForeignKey(
        'breaks.Organisation', models.CASCADE, related_name='groups',
        verbose_name='Организация'
    )
    name = models.CharField('Название', max_length=100)
    manager = models.ForeignKey(
        User, models.RESTRICT, related_name='group_managers',
        verbose_name='Менеджер',
    )
    employees = models.ManyToManyField(
        User, related_name='group_employees', verbose_name='Сотрудники', blank=True,
    )
    min_active = models.PositiveSmallIntegerField(
        'Минимальное кол-во активных сотрудников', null=True, blank=True,
    )
    break_start = models.TimeField('Начало обеда', null=True, blank=True,)
    break_end = models.TimeField('Конец обеда', null=True, blank=True,)
    break_max_duration = models.PositiveSmallIntegerField('Максимальная длительность обеда', null=True, blank=True,)

    class Meta:
        verbose_name = 'Группу'
        verbose_name_plural = 'Группы'
        ordering = ['name']

    def __str__(self):
        return f'{self.name} ({self.pk})'