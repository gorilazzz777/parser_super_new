from django.db import models
from django.utils import timezone

from location.models import City, Route, Package
from tariff_guide.managers.parsing_group import ParsingGroupClassManager
from tariff_guide.managers.parsing_tariff import ParsingTariffClassManager
from tariff_guide.managers.price import PriceManager, PriceClassManager
from tariff_guide.managers.time import DeliveryTimeClassManager, DeliveryTimeManager


class Script(models.Model):
    name = models.CharField('Название', max_length=100)
    code = models.IntegerField('Код', null=True)
    description = models.TextField('Описание сценария', max_length=500, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Сценарий'
        verbose_name_plural = 'Сценарии'


class Direction(models.Model):
    name = models.CharField('Направление (ПиП/ИМ)', max_length=3)
    code = models.IntegerField('Код направления', default=1)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Канал'
        verbose_name_plural = 'Каналы'


class ParsingGroup(models.Model):
    name = models.CharField('Название', max_length=100, null=True)
    script = models.ForeignKey(Script, on_delete=models.CASCADE, verbose_name='Сценарий')
    direction = models.ForeignKey(Direction, verbose_name='Направление', on_delete=models.CASCADE, null=True)
    city = models.ManyToManyField(City, verbose_name='Город', limit_choices_to={'courier_delivery': True,
                                                                                'country_code': 643})
    top_count = models.IntegerField('Кол-во ТОП маршрутов', default=0)
    routes = models.ManyToManyField(Route, verbose_name='Список маршрутов')
    public = models.BooleanField(default=True, verbose_name='Публичная группа')
    subscriber = models.URLField('Подписка на изменение', null=True)
    in_report = models.BooleanField('Отображается в отчете', default=True)



    objects = models.Manager()
    manager = ParsingGroupClassManager()


    def __str__(self):
        return f'{self.name} - {self.direction}'

    class Meta:
        verbose_name = 'Группа парсинга'
        verbose_name_plural = 'Группы парсинга'
        ordering = ['name']


class ApiCodes(models.Model):
    serviсe = models.ForeignKey('parser.Service', on_delete=models.CASCADE, verbose_name='Служба доставки')
    code = models.CharField('Код тарифа', max_length=45)
    tittle = models.CharField('Название тарифа', max_length=45)
    direction = models.ForeignKey(Direction, verbose_name='Направление', on_delete=models.CASCADE, null=True,
                                  blank=True)

    def __str__(self):
        return f'{self.serviсe.name} - {self.tittle} - {self.direction}'

    class Meta:
        verbose_name = 'Код тарифа служб доставок'
        verbose_name_plural = 'Коды тарифов служб доставок'


class ParsingModels(models.Model):
    code = models.CharField('Код Модели', max_length=45)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = 'Модель для парсинга'
        verbose_name_plural = 'Модели для парсинга'


class ParsingTariff(models.Model):
    update = models.DateTimeField('Дата обновления', default=timezone.now)
    tariff = models.ForeignKey('parser.DeliveryTariff', on_delete=models.CASCADE, verbose_name='Тариф',
                               related_name='parsing_tariffs')
    route = models.ForeignKey(Route, on_delete=models.CASCADE, verbose_name='Маршрут')
    is_fast = models.BooleanField('Самый быстрый', default=False)
    is_slowest = models.BooleanField('Самый медленный', default=False)
    time = models.ForeignKey('DeliveryTime', on_delete=models.CASCADE, verbose_name='Сроки доставки',
                             null=True)

    objects = models.Manager()
    manager = ParsingTariffClassManager()

    def __str__(self):
        return f'{self.route} - {self.tariff} - {self.update}'

    class Meta:
        verbose_name = 'Тариф на маршрут'
        verbose_name_plural = 'Тарифы на маршрут'
        indexes = [
            models.Index(fields=['route', 'tariff']),
            models.Index(fields=['is_fast']),
            models.Index(fields=['is_slowest']),
        ]


class DeliveryTime(models.Model, DeliveryTimeManager):
    max = models.IntegerField('Максимальный срок')
    min = models.IntegerField('Минимальный срок')
    cheaper = models.ManyToManyField('parser.DeliveryTariff', related_name='time_cheaper')
    more_expensive = models.ManyToManyField('parser.DeliveryTariff', related_name='time_more_expensive')

    objects = models.Manager()
    manager = DeliveryTimeClassManager()

    def __str__(self):
        return f'от {self.min} до {self.max} дней'

    class Meta:
        verbose_name = 'Срок'
        verbose_name_plural = 'Сроки'


class Price(models.Model, PriceManager):
    package = models.ForeignKey(Package, on_delete=models.CASCADE, verbose_name='Короб')
    price = models.FloatField('Цена', default=0)
    is_min = models.BooleanField('Минимальный на маршруте', default=False)
    is_max = models.BooleanField('Минимальный на маршруте', default=False)
    tariffs = models.ForeignKey(ParsingTariff, verbose_name='Тарифф', related_name='prices', on_delete=models.CASCADE)
    cheaper = models.ManyToManyField('parser.DeliveryTariff', related_name='price_cheaper', verbose_name='Дешевле чем', blank=True)
    more_expensive = models.ManyToManyField('parser.DeliveryTariff', related_name='price_more_expensive',
                                            verbose_name='Дороже чем', blank=True)

    objects = models.Manager()
    manager = PriceClassManager()

    def __str__(self):
        return f'{self.price}'

    class Meta:
        verbose_name = 'Цена'
        verbose_name_plural = 'Цены'
        indexes = [
            models.Index(fields=['package', 'tariffs']),
            models.Index(fields=['is_min']),
            models.Index(fields=['is_max']),
        ]
        ordering = ['package__weight']


class ServiceCustomPackageName(models.Model):
    package = models.ForeignKey(Package, verbose_name='Упаковка', on_delete=models.CASCADE)
    tariff = models.ForeignKey('parser.DeliveryTariff', verbose_name='Тариф', on_delete=models.CASCADE)
    name = models.CharField('Название', max_length=150)
    in_report = models.BooleanField('Отображать в отчете', default=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Кастомное название упаковки'
        verbose_name_plural = 'Кастомные названия упаковок'
        ordering = ['package__weight']
