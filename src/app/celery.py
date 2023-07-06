from __future__ import absolute_import

import json
import os
import threading
import traceback
from datetime import timedelta, datetime

import django

from celery import Celery
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()

app = Celery('app')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task
def update_tariff(_id):
    from parser.models import DeliveryTariff

    tariff = DeliveryTariff.objects.get(id=_id)
    try:
        tariff.update_tariffs()
    except:
        print(traceback.format_exc())
        print(f'{tariff} - {tariff.direction.name} - error!')



@app.task
def update_tariffs(_id):
    from parser.models import DeliveryTariff

    result = []
    threads = []
    for delay_min, i in enumerate(DeliveryTariff.objects.filter(delivery_servise_id=_id)):
        thread = threading.Thread(target=update_tariff, args=(i.id, ))
        threads.append(thread)
        result.append(i.name)
        thread.start()
    return 'Тарифы отработали: ' + ' '.join(result)


@app.task
def create_report_pip():
    from parser.reports.pip_report import PipReport

    PipReport().create_report()


@app.task
def create_report_im():
    from parser.reports.im_report import ImReport

    ImReport().create_report()


@app.task
def beat():
    print(f'time - {timezone.now()}')
    return f'time - {timezone.now()}'

