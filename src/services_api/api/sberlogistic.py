import json
import logging
import traceback

from services_api.api.request_func import request_func
from app.settings import SBERLOGISTIC_GET_POINT_URL, SBERLOGISTIC_CALC_URL_IM, SBERLOGISTIC_CALC_URL_PIP

logger = logging.getLogger("app")


class Sberlogistic:
    def __init__(self):
        self.url = SBERLOGISTIC_GET_POINT_URL
        self.url_calc_im = SBERLOGISTIC_CALC_URL_IM
        self.url_calc_pip = SBERLOGISTIC_CALC_URL_PIP

    def get_points(self, city, delivery_type):
        data = {
            "method": "getDeliveryPoints",
            "params": {
                "kladr_id": city.kladr,
                "shipping_method": 200,
                "self_pick_up": delivery_type,
                "self_pick_up_real_time": delivery_type
            },
            "jsonrpc": "2.0",
            "wk": "P!$$IM?XBQ-V2$DBN1M62BCAJ2--MR33-KLU26941"
        }
        response = request_func(url=self.url, method='POST', data=json.dumps(data), timeout=10)
        if response:
            return response['result']

    def get_data_from_response(self, response, tariff):
        result = {}
        try:
            if response.get('result'):
                for courier in response['result']['methods']:
                    if courier['method']['name'] == tariff.code.code or courier['method']['name'] == tariff.name:
                        price = courier['cost']['total']['sum']
                        result = {
                            'max_day': courier['max_days'],
                            'min_day': courier['min_days'],
                            'price': price + (12 if tariff.direction.name == 'ИМ' else 0)
                        }
                        break
        except:
            logger.error(f'Error in Sber get_data_from_response: {traceback.format_exc()}')
        finally:
            return result

    def calculation_im(self, route, package, tariff):
        if route.sender_city.kladr or route.receiver_city.kladr:
            body = {
                "id": "JsonRpcClient.js",
                "jsonrpc": "2.0",
                "method": "calculateShipping",
                "params": {
                    "courier": tariff.code.code,
                    "stock": True,
                    "kladr_id_from": route.sender_city.kladr[:-2],
                    "kladr_id": route.receiver_city.kladr[:-2],
                    "length": 10,
                    "width": 10,
                    "height": 10,
                    "weight": package.weight,
                    "cod": 0,
                    "declared_cost": 0
                }
            }
            response = request_func(method='POST', url=self.url_calc_im, json=body, timeout=15, try_count=10)
            if response:
                return self.get_data_from_response(response=response, tariff=tariff)
        return {}

    def calculation_pip(self, route, package, tariff):
        if route.sender_city.kladr or route.receiver_city.kladr:
            try:
                body = json.dumps({
                    "jsonrpc": "2.0",
                    "method": "calculateShipping",
                    "params": {
                        "verbose": 1,
                        "kladr_id_from": route.sender_city.kladr,
                        "kladr_id": route.receiver_city.kladr,
                        "country_code": "RU",
                        "weight": package.weight,
                        "length": package.sberlogistic_package.depth,
                        "width": package.sberlogistic_package.width,
                        "height": package.sberlogistic_package.height,
                        "declared_cost": 0,
                        "cod": "0"
                    },
                    "id": "JsonRpcClient.js"
                })
            except:
                print(traceback.format_exc())
                print(12)
            response = request_func(method='POST', url=self.url_calc_pip, data=body, timeout=15, try_count=10)
            if response:
                return self.get_data_from_response(response=response, tariff=tariff)
        return {}

    def calculate(self, route, package, tariff):
        if tariff.direction.code == 1:
            return self.calculation_im(route=route, tariff=tariff, package=package)
        else:
            return self.calculation_pip(route=route, tariff=tariff, package=package)
