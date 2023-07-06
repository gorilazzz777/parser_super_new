import json
import uuid
from datetime import datetime

from app.settings import BILLING_URL, BILLING_CLIENT_ID
from services_api.api.request_func import request_func


class Billing:
    def __init__(self):
        self.url = BILLING_URL
        self.id_client = BILLING_CLIENT_ID

    def calculate(self, route, package, tariff):
        body = {
            "idClient": self.id_client,
            "SenderCityId": route.sender_city.code,
            "RecipientCityId": route.receiver_city.code,
            "OrderSum": 50000,
            "DeliverySum": 0,
            "PaySum": 0,
            "PromoCode": "",
            "BoxSizes": [
                {
                    "Width": 10,
                    "Height": 10,
                    "Depth": 10,
                    "Weight": package.weight * 1000
                }
            ],
            "Issue": "",
            "PayType": "000000112",
            "ResponseIsRequired": 1,
            "MessageDate": datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
            "MessageId": str(uuid.uuid1()),
            "InterfaceType": "DeliveryCostArray",
            "InterfaceVersion": "1.04"
        }

        response = request_func(method='POST', url=self.url, data=json.dumps(body), timeout=10)
        if response and type(response.get('DeliveryCosts')) == list:
            for delivery_type in response['DeliveryCosts']:
                if int(delivery_type['DeliveryTypeId']) == int(tariff.type.code):
                    return {
                        'max_day': delivery_type['DeliveryPeriod'],
                        'min_day': delivery_type['DeliveryPeriod'],
                        'price': float(delivery_type['TotalPrice']),
                    }
