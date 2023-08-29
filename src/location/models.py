from django.db import models
from django.utils import timezone

from location.managers.package import PackageClassManager
from location.managers.route import RouteClassManager


class City(models.Model):
    date = models.DateTimeField(default=timezone.now)
    name = models.CharField('Название', max_length=50)
    region = models.CharField('Область', max_length=60)
    reception_lap = models.BooleanField('Прием', default=False)
    delivery_lap = models.BooleanField('Выдача', default=False)
    code = models.CharField('Код Боксберри', max_length=50)
    courier_delivery = models.BooleanField('Курьерская доставка', default=False)
    kladr = models.CharField('Кладр', max_length=55)
    dpd_code = models.CharField('Код ДПД', max_length=55, null=True)
    bxb_point_code = models.CharField('Код ПВЗ ББ', max_length=55, null=True, blank=True)
    cdek_code = models.IntegerField('Код СДЭК', null=True, blank=True)
    cdek_uuid = models.UUIDField('UUID СДЭК', null=True, blank=True)
    country_code = models.CharField('Код страны', default=643, max_length=5)

    def __str__(self):
        return f'{str(self.name)} ({self.region})'

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['country_code'])
        ]


class PointType(models.Model):
    name = models.CharField('Название типа', max_length=20)


class Point(models.Model):
    delivery_service = models.ForeignKey('parser.Service', on_delete=models.CASCADE,
                                         verbose_name='Служба доставки', null=True)
    update_date = models.DateTimeField(default=timezone.now)
    code = models.CharField('Код', max_length=12)
    address = models.CharField('Адресс', max_length=200)
    courier = models.CharField('Партнер', max_length=50, null=True)
    latitude = models.FloatField('Широта', null=True)
    longitude = models.FloatField('Долгота', null=True)
    kladr = models.CharField('КЛАДР', max_length=25, null=True)
    reception_lap = models.BooleanField('Прием', default=False)
    delivery_lap = models.BooleanField('Выдача', default=False)
    active = models.BooleanField('Действующая', default=True)
    type = models.ForeignKey(PointType, on_delete=models.CASCADE, verbose_name='Тип отделения', null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='points')
    zip = models.IntegerField(null=True)

    def __str__(self):
        return self.address

    class Meta:
        verbose_name = 'Пункт выдачи'
        verbose_name_plural = 'Пункты выдачи'

        indexes = [
            models.Index(fields=['code'])
        ]


class Zip(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name='Город', related_name='zips')
    zip = models.IntegerField('Индекс')
    in_calc = models.BooleanField('Учавствует в рассчете', default=True)

    class Meta:
        verbose_name = 'Индекс'
        verbose_name_plural = 'Индексы'

        indexes = [
            models.Index(fields=['zip'])
        ]


class Zone(models.Model):
    code = models.CharField('Код тарифной зоны', max_length=5)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = 'Зона'
        verbose_name_plural = 'Зоны'


class Route(models.Model):
    sender_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='sender_cities',
                                    verbose_name='Город отправитель', limit_choices_to={'delivery_lap': True,
                                                                                        'country_code': 643})
    receiver_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='receiver_cities',
                                      verbose_name='Город получатель', limit_choices_to={'delivery_lap': True,
                                                                                         'country_code': 643})
    zone = models.ForeignKey(Zone, on_delete=models.SET_NULL, verbose_name='Зона', null=True, related_name='routes')
    zone_avito = models.ForeignKey(Zone, on_delete=models.SET_NULL, verbose_name='Зона Авито', null=True, blank=True,
                                   related_name='routes_avito')
    time = models.IntegerField(null=True, blank=True)

    objects = models.Manager()
    manager = RouteClassManager()

    def __str__(self):
        return f'{self.sender_city.name} - {self.receiver_city.name}'

    def name(self):
        return f'{self.sender_city.name} - {self.receiver_city.name}'

    class Meta:
        verbose_name = 'Маршрут'
        verbose_name_plural = 'Маршруты'

        indexes = [
            models.Index(fields=['sender_city', 'receiver_city'])
        ]


class DeliveryType(models.Model):
    name = models.CharField('Название', max_length=50)
    code = models.IntegerField('Код')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тип доставки'
        verbose_name_plural = 'Типы доставки'


class Package(models.Model):
    code = models.CharField('Код', max_length=3, null=True, blank=True)
    name = models.CharField('Название', max_length=40, null=True, blank=True)
    height = models.IntegerField('Высота', null=True, blank=True)
    depth = models.IntegerField('Длина', null=True, blank=True)
    width = models.IntegerField('Ширина', null=True, blank=True)
    weight = models.FloatField('Вес')
    dpd_shop_name = models.CharField('Название короба в DPD Shop', max_length=40, null=True, blank=True)
    pony_express_name = models.CharField('Название короба в PonyExpress', max_length=40, null=True, blank=True)
    cdek_box_name = models.CharField('Название короба в CDEK Посылочка', max_length=40, null=True, blank=True)
    sberlogistic_package = models.ForeignKey('DeliveryServicePackage', on_delete=models.SET_NULL,
                                             verbose_name='Короб Сберлогистики', null=True, blank=True)
    cdek_box_package = models.ForeignKey('DeliveryServicePackage', on_delete=models.SET_NULL,
                                             verbose_name='Короб СДЭК Посылочки', null=True, blank=True,
                                         related_name='cdek_box_package')
    value = models.FloatField('Объем', null=True, blank=True)
    pip = models.BooleanField('ПиП', default=True)
    in_report = models.BooleanField('В отчете ПиП', default=True)

    objects = models.Manager()
    manager = PackageClassManager()

    def __str__(self):
        return f'{self.weight} кг'

    class Meta:
        verbose_name = 'Упаковка'
        verbose_name_plural = 'Упаковки'
        ordering = ['weight']


class DeliveryServicePackage(models.Model):
    code = models.CharField('Код', max_length=3, null=True, blank=True)
    name = models.CharField('Название', max_length=40, null=True)
    delivery_tariff = models.ForeignKey('parser.DeliveryTariff', on_delete=models.CASCADE,
                                        verbose_name='Тариф', null=True)
    height = models.IntegerField('Высота', null=True)
    depth = models.IntegerField('Длина', null=True)
    width = models.IntegerField('Ширина', null=True)
    weight = models.FloatField('Вес', null=True)

    def __str__(self):
        return f'{self.name} - {self.delivery_tariff}'

    class Meta:
        verbose_name = 'Кастомные параметры упаковки'
        verbose_name_plural = 'Кастомные параметры упаковок'
        ordering = ['weight']
