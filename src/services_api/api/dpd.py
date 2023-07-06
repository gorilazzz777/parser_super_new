from app.settings import DPD_CLIENT_KEY, DPD_CLIENT_NUMBER, DPD_API_URL_GEO, DPD_API_URL_CALC

from services_api.api.request_func import request_func


class Dpd:
    def __init__(self):
        self.url_geo = DPD_API_URL_GEO
        self.url_calc = DPD_API_URL_CALC
        self.headers = {'content-type': 'text/xml'}
        self.client_key = DPD_CLIENT_KEY
        self.client_number = DPD_CLIENT_NUMBER

    def get_cities(self):
        body = f"""<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns="http://dpd.ru/ws/geography/2015-05-20">
           <soapenv:Header/>
           <soapenv:Body>
              <ns:getCitiesCashPay>
                 <request>
                    <auth>
                       <clientNumber>{self.client_number}</clientNumber>
                       <clientKey>{self.client_key}</clientKey>
                    </auth>
                    <countryCode>RU</countryCode>
                 </request>
              </ns:getCitiesCashPay>
           </soapenv:Body>
        </soapenv:Envelope>"""
        response = request_func(url=self.url_geo, method='POST', headers=self.headers, data=body, timeout=10)
        if response:
            cities = response['S:Envelope']['S:Body']['ns2:getCitiesCashPayResponse']['return']
            result = {}
            for city in cities:
                result[city['cityCode']] = {
                    'indexMin': city.get('indexMin'),
                    'indexMax': city.get('indexMax'),
                    'cityId': city.get('cityId')
                }
            return result

    def get_points(self):
        data = f'''
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns="http://dpd.ru/ws/geography/2015-05-20">
   <soapenv:Header/>
   <soapenv:Body>
      <ns:getParcelShops>
         <!--Optional:-->
         <request>
            <auth>
               <clientNumber>{self.client_number}</clientNumber>
               <clientKey>{self.client_key}</clientKey>
            </auth>
            <!--Optional:-->
            <countryCode>RU</countryCode>
         </request>
      </ns:getParcelShops>
   </soapenv:Body>
</soapenv:Envelope>
        '''
        response = request_func(url=self.url_geo, method='POST', headers=self.headers, data=data, timeout=40)
        if response:
            points = response['S:Envelope']['S:Body']['ns2:getParcelShopsResponse']['return'][
                'parcelShop']
            return points

    def body_calc(self, route, body):
        return f"""<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns="http://dpd.ru/ws/calculator/2012-03-20">
           <soapenv:Header/>
           <soapenv:Body>
              <ns:getServiceCost2>
                 <request>
                    <auth>
                       <clientNumber>{self.client_number}</clientNumber>
                       <clientKey>{self.client_key}</clientKey>
                    </auth>
                    <pickup>
                       <cityId>{route.sender_city.dpd_code}</cityId>
                    </pickup>
                    <delivery>
                       <cityId>{route.receiver_city.dpd_code}</cityId>
                    </delivery>
                    <selfPickup>1</selfPickup>
                    {body}
                 </request>
              </ns:getServiceCost2>
           </soapenv:Body>
        </soapenv:Envelope>"""

    def calculate(self, route, package, tariff):
        if tariff.type.code == 3:
            body = self.body_calc(route, f'<selfDelivery>0</selfDelivery>'
                                    f'<weight>{package.weight}</weight>')
        elif tariff.code.code == 'PUP':
            body = self.body_calc(route, f'<selfDelivery>1</selfDelivery>'
                                    f'<weight>1</weight>'
                                    f'<volume>{package.value}</volume>')
        else:
            body = self.body_calc(route, f'<selfDelivery>1</selfDelivery>'
                                    f'<weight>{package.weight}</weight>')
        response = request_func(method='POST', url=self.url_calc, headers=self.headers, data=body, timeout=40)
        if response:
            costs = response['S:Envelope']['S:Body']['ns2:getServiceCost2Response']['return']
            for cost in costs:
                if cost['serviceCode'] == tariff.code.code:
                    if tariff.delivery_servise.sale:
                        if tariff.code.code == 'PUP':
                            price = round(float(cost['cost']) / 0.8)
                        else:
                            price = (float(cost['cost']) - 60) / 0.8 + 60
                    else:
                        price = float(cost['cost'])
                    return {
                        'max_day': cost['days'],
                        'min_day': cost['days'],
                        'price': round(price, 2)
                    }
        return {}
