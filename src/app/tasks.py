from __future__ import absolute_import, unicode_literals

import traceback
from datetime import datetime, timedelta

from app.celery import app

from django.utils import timezone

from parser.models import DeliveryTariff
from parser.reports.im_report import ImReport
from parser.reports.pip_report import PipReport


@app.task
def update_tariff(_id):
    start = datetime.now()
    tariff = DeliveryTariff.objects.get(id=_id)
    print(f'start {tariff} - {tariff.direction.name} - {start}')
    try:
        tariff.update_tariffs()
    except:
        print(traceback.format_exc())
        print(f'{tariff} - {tariff.direction.name} - error!')
    stop = datetime.now()
    print(f'{tariff} - {tariff.direction.name} - {stop - start}')


@app.task
def update_tariffs():
    for delay_min, i in enumerate(DeliveryTariff.objects.all()):
        time = timezone.now() + timedelta(minutes=delay_min + 1)
        update_tariff.apply_async(
            args=[i.id],
            eta=time)
        print(f'start at {i} - {i.direction.name} - {delay_min + 1}')


@app.task
def create_report_pip():
    PipReport().create_report()


@app.task
def create_report_im():
    ImReport().create_report()


@app.task
def beat():
    print(f'time - {timezone.now()}')
