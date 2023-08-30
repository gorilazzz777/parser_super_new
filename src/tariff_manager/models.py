from django.db import models

from src.location.models import Package, Route


class Price(models.Model):
    calc = models.IntegerField('Цена в Трификаторе', null=True)
    parser = models.IntegerField('Цена тарифа который парсим', null=True)
    current = models.IntegerField('Текущая установленная цена', null=True)

    def __str__(self):
        return str(self.current)

    class Meta:
        verbose_name = 'Цена'
        verbose_name_plural = 'Цены'


class Tariff(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, verbose_name='Маршрут')
    package = models.ForeignKey(Package, on_delete=models.CASCADE, verbose_name=' Упаковка')
    price = models.OneToOneField(Price, verbose_name='Цена', on_delete=models.SET_NULL)

    def __str__(self):
        return f'{str(self.route)} - {self.package}'

    class Meta:
        verbose_name = 'Тариф'
        verbose_name_plural = 'Тарифы'
        indexes = [
            models.Index(fields=['route', 'package'])
        ]
