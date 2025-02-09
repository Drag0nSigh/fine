from django.contrib.auth.models import AbstractUser, Group, Permission

from django.db import models

from core.constants import (
    ADMIN,
    MAX_LENGTH_ID_TG,
    MAX_LENGTH_ROLE,
    MAX_LENGTH_USERNAME,
    USER,
    USER_ROLE_CHOICES,
)


class CustomUser(AbstractUser):
    groups = models.ManyToManyField(
        Group,
        verbose_name="groups",
        blank=True,
        help_text="Группы, к которым принадлежит этот пользователь.",
        related_name="custom_user_set",
        related_query_name="custom_user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name="user permissions",
        blank=True,
        help_text="Конкретные разрешения для этого пользователя.",
        related_name="custom_user_set",
        related_query_name="custom_user",
    )

    username = models.CharField(
        verbose_name='Никнейм',
        max_length=MAX_LENGTH_USERNAME,
        unique=True,
        help_text=f'Обязательное поле. Максимальная длина '
                  f'{MAX_LENGTH_USERNAME} символов.'
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=MAX_LENGTH_ROLE,
        choices=USER_ROLE_CHOICES,
        default=USER,
    )
    tg_id = models.CharField(
        verbose_name='id telegram',
        max_length=MAX_LENGTH_ID_TG,
        help_text='id telegram'
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email

    @property
    def is_admin(self):
        return self.role == ADMIN or self.is_superuser
