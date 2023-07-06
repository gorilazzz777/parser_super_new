from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from location.models import City, Route, DeliveryType, Package
from parser.managers.delivery_tariff import DeliveryTariffManager
from tariff_guide.models import Direction, ParsingGroup

Users = get_user_model()


class UserProfile(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True, verbose_name='profile')
    report_pip = models.BooleanField(default=False, verbose_name='Рассылка парсинга ПиП')
    report_im = models.BooleanField(default=False, verbose_name='Рассылка парсинга ИМ')
    report_point = models.BooleanField(verbose_name='Рассылка ПВЗ', default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'


class Service(models.Model):
    date = models.DateTimeField('Дата добавления', default=timezone.now)
    name = models.CharField('Название', max_length=50)
    sale = models.BooleanField('Скидка', default=False)
    can_add = models.BooleanField('Можно ли добавить тариф', default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Служба Доставки'
        verbose_name_plural = 'Службы Доставки'


class DeliveryTariff(models.Model, DeliveryTariffManager):
    delivery_servise = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name='Служба доставки', null=True)
    name = models.CharField('Название', max_length=50)
    code = models.ForeignKey('tariff_guide.ApiCodes', verbose_name='Код тарифа', on_delete=models.CASCADE,
                             null=True, blank=True)
    type = models.ForeignKey(DeliveryType, on_delete=models.CASCADE, verbose_name='Тип Доставки')
    direction = models.ForeignKey(Direction, verbose_name='Направление', on_delete=models.CASCADE)
    limit = models.IntegerField('Кол-во маршрутов в час', default=40)
    in_statistic = models.BooleanField(default=False)
    parsing_groups = models.ManyToManyField(ParsingGroup, verbose_name='Группы парсинга')
    packages = models.ManyToManyField(Package, verbose_name='Упаковки для парсинга')
    in_report = models.BooleanField('Выгружать в отчет', default=True)
    in_parser = models.BooleanField('Создание по api', default=False)
    distinct_key = models.CharField('Ключ для оптимизации выбора короба', max_length=40, null=True, blank=True)
    parsing_model = models.ForeignKey('tariff_guide.ParsingModels', verbose_name='Модель для парсинга тарифа',
                                      on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.delivery_servise.name} {self.name} {self.direction.name}'

    class Meta:
        verbose_name = 'Тариф на доставку'
        verbose_name_plural = 'Тарифы на доставку'