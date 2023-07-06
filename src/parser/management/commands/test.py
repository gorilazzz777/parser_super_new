import json
from datetime import timedelta, datetime

from django.core.management.base import BaseCommand
from django.forms import model_to_dict
from django.utils import timezone

from location.models import City, Route
from parser.helpers import query_debugger
from parser.models import DeliveryTariff, Service
from app.tasks import update_tariff
from parser.serializers import ServiceSerializer
from services_api.api.request_func import request_func
from tariff_guide.models import ParsingTariff


def get_token():
    params = {
        'grant_type': 'client_credentials',
        'client_id': 'I34kcPGDmFRRYSaG9RfTAmVwngB9xy0i',
        'client_secret': 'uNqqN3Ei06tfuzJrgCOM2BtdD8Cuioho'
    }
    response = request_func('https://api.cdek.ru/v2/oauth/token', params=params, method='POST')
    if response:
        return response['access_token']
    raise ValueError('Авторизация провалилиась')


class Command(BaseCommand):
    help = 'обновление тарифов'

    def handle(self, *args, **kwargs) -> None:
        # cities = request_func(url='https://api.cdek.ru/v2/location/cities/?country_codes=RU&size=10000', headers={
        #     'Authorization': f'Bearer {get_token()}',
        #     'Content-Type': 'application/json'
        # }, timeout=20)
        # for city in cities:
        #     c = City.objects.filter(cdek_code=city['code']).first()
        #     if c and c.cdek_uuid is None:
        #         c.cdek_uuid = city['city_uuid']
        #         c.save()
        #         print(c.name)
        route = Route.objects.filter(sender_city__name='Новый Уренгой', receiver_city__name='Хабаровск').first()
        DeliveryTariff.objects.get(id=96).update_tariffs(route=route)
        # for delay_min, i in enumerate(DeliveryTariff.objects.all()):
        #     print(i, i.direction)
        #     i.update_tariffs()
        #     update_tariff.apply_async(
        #         args=[i.id],
        #         eta=timezone.now() + timedelta(minutes=delay_min+1))
        #
        # print(datetime.now() - s)