import json

from app.settings import LKP_API_URL, LKP_API_STANDARD_TOKEN
from services_api.api.request_func import request_func


class ApiLKP:
    def __init__(self, api_token=None):
        self.url = LKP_API_URL
        self.api_token = api_token if api_token else LKP_API_STANDARD_TOKEN

    def get_indexes(self, city_code):
        params = {
            'api_token': self.api_token,
            'method': 'ListPoints',
            'city': city_code
        }
        response = request_func(url=self.url, params=params)
        if response and response.get('data'):
            result = []
            for point in response.get('data'):
                result.append(point['address'].split(',')[0])
            return list(set(result))

    def calculate(self, route, package, tariff):
        price = 50000
        body = {
            'api_token': self.api_token,
            'method': 'CalculationLaP',
            'public_price': price,
            'sender_city': route.sender_city.code,
            'receiver_city': route.receiver_city.code,
            'package': {
                'boxberry_package': 1,
                'package_code': package.code,
            },
        }
        response = request_func(method='POST', url=f'{self.url}?method=CalculationLaP', data=json.dumps(body))
        if response and response.get('data') and type(response['data']) == list:
            for delivery_type in response['data']:
                if int(tariff.type.code) == int(delivery_type['delivery_type']):
                    return {
                        'max_day': delivery_type.get('time'),
                        'min_day': delivery_type.get('time'),
                        'price': delivery_type.get('price') / 100
                    }