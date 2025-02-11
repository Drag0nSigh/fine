from django.db import models


class Car(models.Model):
    """
    Автомобиль по которому будет проверяться штрафы
    """
    group_id = models.IntegerField(
        verbose_name='Идентификатор подразделения',
        blank=True,
    )
    auto_cdi = models.CharField(
        verbose_name='СТС автомобиля',
        blank=True,
        max_length=10,
    )
    auto_number = models.CharField(
        verbose_name='Госномер авто (без региона)',
        blank=True,
        max_length=6,
    )
    auto_region = models.CharField(
        verbose_name='Регион госномера авто',
        blank=True,
        max_length=3
    )
    auto_name = models.CharField(
        verbose_name='Название автомобиля',
        blank=True,
    )
    valid_number = models.BooleanField(
        verbose_name='Статус госномера',
        default=False,
        null=True,
    )
    check_platon = models.BooleanField(
        verbose_name='Проверяются штрафы за Платон',
        default=False,
    )
    owner_inn = models.CharField(
        verbose_name='ИНН собственника авто',
        blank=True,
        max_length=10,
    )
    auto_vin = models.CharField(
        verbose_name='VIN номер авто',
        blank=True,
        max_length=20
    )
    check_auto = models.BooleanField(
        verbose_name='Включена проверка автомобиля на ДТП, '
                     'ограничения и залог',
        default=False,
    )
    check_pass = models.BooleanField(
        verbose_name='Включена проверка пропуска в Москву',
        default=False,
    )
    external_id = models.IntegerField(
        verbose_name='ID из внешней системы',
        unique=True,
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Машина'
        verbose_name_plural = 'Машины'
