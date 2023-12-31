# Generated by Django 4.2.1 on 2023-06-22 20:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import parser.managers.delivery_tariff


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата добавления')),
                ('name', models.CharField(max_length=50, verbose_name='Название')),
                ('sale', models.BooleanField(default=False, verbose_name='Скидка')),
                ('can_add', models.BooleanField(default=False, verbose_name='Можно ли добавить тариф')),
            ],
            options={
                'verbose_name': 'Служба Доставки',
                'verbose_name_plural': 'Службы Доставки',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report_pip', models.BooleanField(default=False, verbose_name='Рассылка парсинга ПиП')),
                ('report_im', models.BooleanField(default=False, verbose_name='Рассылка парсинга ИМ')),
                ('report_point', models.BooleanField(default=False, verbose_name='Рассылка ПВЗ')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='profile')),
            ],
            options={
                'verbose_name': 'Профиль пользователя',
                'verbose_name_plural': 'Профили пользователей',
            },
        ),
        migrations.CreateModel(
            name='DeliveryTariff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Название')),
                ('code', models.CharField(max_length=50, verbose_name='Код тарифа')),
                ('limit', models.IntegerField(default=40, verbose_name='Кол-во маршрутов в час')),
                ('in_statistic', models.BooleanField(default=False)),
                ('in_report', models.BooleanField(default=True, verbose_name='Выгружать в отчет')),
                ('in_parser', models.BooleanField(default=False, verbose_name='Создание по api')),
                ('distinct_key', models.CharField(blank=True, max_length=40, null=True, verbose_name='Ключ для оптимизации выбора короба')),
                ('parsing_model', models.CharField(max_length=40, null=True, verbose_name='Модель для парсинга тарифа')),
                ('delivery_servise', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='parser.service', verbose_name='Служба доставки')),
            ],
            options={
                'verbose_name': 'Тариф на доставку',
                'verbose_name_plural': 'Тарифы на доставку',
            },
            bases=(models.Model, parser.managers.delivery_tariff.DeliveryTariffManager),
        ),
    ]
