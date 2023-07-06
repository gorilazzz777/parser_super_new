# Generated by Django 4.2.1 on 2023-06-28 11:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tariff_guide', '0004_parsingmodels'),
        ('parser', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deliverytariff',
            name='code',
        ),
        migrations.RemoveField(
            model_name='deliverytariff',
            name='parsing_model',
        ),
        migrations.AddField(
            model_name='deliverytariff',
            name='code',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tariff_guide.apicodes', verbose_name='Код тарифа'),
        ),
        migrations.AddField(
            model_name='deliverytariff',
            name='parsing_model',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tariff_guide.parsingmodels', verbose_name='Модель для парсинга тарифа'),
        ),
    ]