import json
import logging
import traceback

from bs4 import BeautifulSoup

from services_api.api.request_func import request_func

logger = logging.getLogger("app")

class Cdek:
    def __init__(self):
        self.url = 'https://api.cdek.ru/v2/calculator/tariff'
        # self.url_for_calc = 'https://www.cdek-calc.ru/blocks/calc.php'
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


    def get_points(self):
        data = {
            "operationName": "websiteOffices",
            "variables": {
                "filter": {
                    "locale": "ru",
                    "websiteId": "ru",
                    "countryName": "Россия"
                }
            },
            "query": "query websiteOffices($filter: WebsiteEntityOfficeFilter, $sort: WebsiteEntityOfficeSort, $multisort: [WebsiteEntityOfficeSort]) {\n  websiteOffices(filter: $filter, sort: $sort, multisort: $multisort) {\n    id\n    type\n    geoLatitude\n    geoLongitude\n    cityCode\n    city\n    fiasCode\n    address\n}\n}\n"
        }
        response = request_func(method='POST', http=True, url=self.url, body=json.dumps(data))
        return response['data']['websiteOffices']

    def calculate(self, route, package, tariff):
        if route.sender_city.cdek_code and route.receiver_city.cdek_code:
            data = {
                "type": "1",
                "currency": "1",
                "tariff_code": str(tariff.code.code),
                "from_location": {
                    "code": route.sender_city.cdek_code

                },
                "to_location": {
                    "code": route.receiver_city.cdek_code
                },

                "packages": [
                    {
                        "weight": int(package.weight * 1000)

                    }
                ]
            }
            if tariff.direction.name == 'ПиП':
                data['packages'][0]['length'] = package.depth
                data['packages'][0]['width'] = package.width
                data['packages'][0]['height'] = package.height
            response = None
            for _ in range(2):
                response = request_func(method='POST', url=self.url, json=data, timeout=15, headers=self.heareds, need_400=True)
                if response:
                    break
                self.heareds = {
                    'Authorization': f'Bearer {self.get_token()}',
                    'Content-Type': 'application/json'
                }
            if response:
                if response.get('total_sum'):
                    try:
                        print(f'{tariff} - {route} - {package.weight} - {response["total_sum"]}')
                        return {
                            'max_day': response['period_max'],
                            'min_day': response['period_min'],
                            'price': response['total_sum']
                        }
                    except:
                        logger.error(f'Error calc CDEK. Error - {traceback.format_exc()} \n')
                return {}
            print(f'{tariff} - {route} - {package.weight} - нет цены')
        return {}