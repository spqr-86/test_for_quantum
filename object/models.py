from django.db import models
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _


User = get_user_model()


class Object(models.Model):
    STATUS_CHOICES = [
        ('created', _('создан')),
        ('launched', _('запущен')),
        ('stopped', _('остановлен')),
    ]
    priority = models.PositiveSmallIntegerField(
        verbose_name=_('Приоритет'),
        validators=[
            MaxValueValidator(100),
        ]
    )
    status = models.CharField(
        verbose_name=_('Статус'),
        max_length=20,
        default='created',
        choices=STATUS_CHOICES,
    )
    time_of_creation = models.DateTimeField(
        verbose_name=_('Время создания'),
        default=now,
    )
    performers = models.ManyToManyField(
        User,
        verbose_name=_('Список исполнителей'),
        blank=True,
        null=True,
    )

    def __str__(self):
        return f'id: {self.id}, priority: {self.priority}, status:{self.status}'

    @classmethod
    def create(cls, **kwargs):
        new_object = cls(**kwargs)
        new_object.save()
        return new_object

    @classmethod
    def destroy(cls):
        cls.objects.last().delete()

    @classmethod
    def choose(cls):
        return cls.objects.filter(
            Q(status='created') | Q(status='stopped')
        ).order_by('-priority', 'time_of_creation')[0]
