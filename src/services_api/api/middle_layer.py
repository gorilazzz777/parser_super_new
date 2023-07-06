import uuid

from app.settings import MA_TOKEN, MA_URL

from .request_func import request_func


class ApiML:
    def __init__(self):
        self.headers = {
            'Authorization': f"Bearer {MA_TOKEN}",
            'Content-Type': 'application/json',
            'X-Request-Id': str(uuid.uuid1())
        }
        self.url = MA_URL

    def list_cities(self, offset=0, code=None, delivery_lap=None, country_code=None):
        if code:
            params = {
                "cityCode": code
            }
        else:
            params = {
                # 'countryCode': 643,
                'page.offset': offset * 5000,
                'page.limit': 5000,
            }
        if country_code:
            params['countryCode'] = country_code
        if delivery_lap:
            params['deliveryLap'] = 'true'
        response = request_func(f'{self.url}cities', params=params, headers=self.headers, timeout=60)
        if response:
            return response.get('cities')

    def list_points(self, code=None, issuance_boxberry=None, reception=None, returned_fields=None):
        params = {}
        if code:
            params['cityCode'] = code
        if issuance_boxberry:
            params['issuance_boxberry'] = 'true'
        if reception:
            params['reception'] = 'true'
        if returned_fields:
            params['returnedFields'] = returned_fields
        response = request_func(f'{self.url}points', params=params, headers=self.headers, timeout=120)
        if response:
            return response.get('points')

    def get_delivery_price(self, track_num):
        params = {
            'trackNumbers': track_num
        }
        response = request_func(f'{self.url}parcel', params=params, headers=self.headers)
        if response:
            return response.get('parcels')[0]['amountPay']


    def list_statuses(self, orders):
        params = {
            'trackNumbers': orders,
            'sort': 1
        }
        response = request_func(f'{self.url}parcel/status-parcels', params=params, headers=self.headers, timeout=30)
        if response:
            return response.get('parcels')
