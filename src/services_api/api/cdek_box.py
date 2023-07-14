import json
import logging

from app.settings import CDEK_BOX_URL, CDEK_BOX_COST_URL, CDEK_URL_FOR_CITY_UUID
from services_api.api.request_func import request_func

logger = logging.getLogger("app")


class CdekBox:
    def __init__(self):
        self.current_time = {}
        self.url = CDEK_BOX_URL
        self.url_for_cost = CDEK_BOX_COST_URL
        self.url_for_city_uuid = 'https://api.cdek.ru/v2/location/cities/'
        self.url_for_time = 'https://www.cdek.ru/ru/cabinet/api/estimateV2'
        self.heareds = {
            'Authorization': f'Bearer {self.get_token()}',
            'Content-Type': 'application/json'
        }

    def get_token(self):
        params = {
            'grant_type': 'client_credentials',
            'client_id': 'I34kcPGDmFRRYSaG9RfTAmVwngB9xy0i',
            'client_secret': 'uNqqN3Ei06tfuzJrgCOM2BtdD8Cuioho'
        }
        response = request_func('https://api.cdek.ru/v2/oauth/token', params=params, method='POST')
        if response:
            return response['access_token']
        raise ValueError('Авторизация провалилиась')

    def get_city_uuid(self, city):
        if city.cdek_uuid is None:
            params = {
                'code': city.cdek_code
            }
            response = request_func(url=self.url_for_city_uuid, params=params, headers=self.heareds)
            if response:
                city.cdek_uuid = response[0]['city_uuid']
                city.save()
        return str(city.cdek_uuid)

    def get_time(self, package, tariff, route):
        result = {}
        data = {
            "payerType": "sender",
            "currencyMark": "RUB",
            "senderCityId": self.get_city_uuid(route.sender_city),
            "receiverCityId": self.get_city_uuid(route.receiver_city),
            "packages": [
                {
                    "height": package.cdek_box_package.height,
                    "length": package.cdek_box_package.depth,
                    "width": package.cdek_box_package.width,
                    "weight": package.cdek_box_package.weight
                }
            ]
        }
        response = request_func(method='POST', url=self.url_for_time, json=data)
        if response:
            response = response['data']
            if response:
                price = 100000
                s = reversed(response[0]['tariffs'])
                for cdek_tariff in s:
                    if cdek_tariff['serviceId'] != '3e0900c7-18f1-4128-9d85-545143235849' and cdek_tariff['price'] < price:
                        price = cdek_tariff['price']
                        result = {
                                'max_day': cdek_tariff['durationMax'],
                                'min_day': cdek_tariff['durationMin'],
                                'service_id': cdek_tariff['serviceId'],
                            }
            return {
                'max_day': result['max_day'],
                'min_day': result['min_day'],
            }, result['service_id']

    def get_cost(self, data):
        response = request_func(method='POST', url=self.url_for_cost, json=data, headers={
            'Content-Type': 'application/json',
            'Host': 'www.cdek.ru',
            'Origin': 'https://www.cdek.ru',
            'Referer': 'https://www.cdek.ru/ru/box'
        })
        if response and response.get('data') and response['data'].get('loyalty'):
            return response['data'].get('loyalty')['totalPrice']

    def calculate(self, route, package, tariff):
        if route.sender_city.cdek_code is None or route.receiver_city.cdek_code is None:
            return {}
        time, service_id = self.get_time(package, tariff, route)
        data = {
            "withoutAdditionalServices": 1,
            "serviceId": service_id,
            "mode": "OFFICE-OFFICE",
            "payerType": "sender",
            "currencyMark": "RUB",
            "senderCityId": self.get_city_uuid(route.sender_city),
            "receiverCityId": self.get_city_uuid(route.receiver_city),
            "packages": [
                {
                    "length": package.cdek_box_package.depth,
                    "width": package.cdek_box_package.width,
                    "height": package.cdek_box_package.height,
                    "weight": package.cdek_box_package.weight
                }
            ],
            "cashOnDeliveryIndividual": 0
        }
        if time:
            cost = self.get_cost(data)
            if cost:
                return {
                    'max_day': time['max_day'],
                    'min_day': time['min_day'],
                    'price': cost
                }
        return {}
