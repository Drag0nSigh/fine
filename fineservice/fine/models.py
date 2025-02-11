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


class Fine(models.Model):
    external_id = models.IntegerField(
        verbose_name='ID из внешней системы',
        unique=True,
    )
    auto_id = models.IntegerField(
        verbose_name='Идентификатор автомобиля/собственника',
        blank=False,
        null=False,
    )
    auto_group_id = models.IntegerField(
        verbose_name='Идентификатор подразделения',
        blank=True,
        null=True,
    )
    auto_cdi = models.CharField(
        verbose_name='СТС автомобиля',
        blank=True,
        null=True,
        max_length=10,
    )
    gis_id = models.IntegerField(
        verbose_name='Идентификатор штрафа',
        unique=True,
        blank=False,
        null=False,
    )
    gis_status = models.CharField(
        verbose_name='Статус штрафа: nopayed - неоплаченный, '
                     'payed - оплаченный',
        max_length=7,
        blank=False,
        null=False,
    )
    bill_id = models.CharField(
        verbose_name='Номер постановления',
        max_length=30,
        unique=True,
        blank=False,
        null=False,
    )
    pay_bill_date = models.DateField(
        verbose_name='Дата постановления',
        blank=False,
        null=False,
    )
    last_bill_date = models.DateField(
        verbose_name='Дата, до которой нужно оплатить постановление',
        blank=False,
        null=False,
    )
    pay_bill_amount = models.FloatField(
        verbose_name='Сумма штрафа',
        blank=False,
        null=False,
    )
    gis_podrazdelenie = models.CharField(
        verbose_name='Подразделение, вынесшее штраф',
        blank=False,
        null=False,
    )
    gis_inn = models.CharField(
        verbose_name='ИНН получателя',
        blank=False,
        null=False,
        max_length=20,
    )
    gis_kpp = models.CharField(
        verbose_name='КПП получателя',
        max_length=20,
        blank=False,
        null=False,
    )
    gis_send_to = models.CharField(
        verbose_name='Наименование получателя',
    )
    gis_bik = models.CharField(
        verbose_name='БИК банка получателя',
    )
    gis_bank = models.CharField(
        verbose_name='Наименование банка получателя'
    )
    gis_kor_schet = models.CharField(
        verbose_name='Корреспондентский счёт',
        max_length=20
    )
    gis_schet = models.CharField(
        verbose_name='Номер счета получателя',
        max_length=20
    )
    gis_kbk = models.CharField(
        verbose_name='КБК'
    )
    gis_wireoktmo = models.CharField(
        verbose_name='ОКТМО',
    )
    gis_discount = models.IntegerField(
        verbose_name='Размер скидки',
        blank=False,
        null=False,
    )
    gis_discount_uptodate = models.DateField(
        verbose_name='Дата действия скидки',
        blank=False,
        null=False,
    )
    pay_bill_amount_with_discount = models.FloatField(
        verbose_name='Сумма с учетом скидки',
        blank=False,
        null=False,
    )
    offense_location = models.CharField(
        verbose_name='Место нарушения',
    )
    offense_date = models.DateField(
        verbose_name='Дата нарушения',
        blank=False,
        null=False,
    )
    offense_time = models.TimeField(
        verbose_name='Время нарушения',
        blank=False,
        null=False,
    )
    offense_article_number = models.CharField(
        verbose_name='Номер статьи КоАП',
    )
    offense_article = models.CharField(
        verbose_name='Описание статьи КоАП',
    )
    offense_longitude = models.CharField(
        verbose_name='Долгота координаты места нарушения',
    )
    offense_latitude = models.CharField(
        verbose_name='Широта координаты места нарушения',
    )
    ckad_due_date = models.DateField(
        verbose_name='	Срок оплаты задолженности ЦКАД, чтобы штраф был '
                     'отменен. Передается только по штрафам за неоплату '
                     'проезда по ЦКАД'
    )
    ckad_travel_date = models.DateField(
        verbose_name='	Дата проезда по ЦКАД, который не был оплачен. '
                     'Передается только по штрафам за неоплату проезда по ЦКАД'
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Штраф'
        verbose_name_plural = 'Штрафы'
