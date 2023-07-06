from app.settings import POCHTA_API_URL
from location.models import Zip
from services_api.api.LKP import ApiLKP
from services_api.api.request_func import request_func


class Pochta:
    def __init__(self):
        self.url = POCHTA_API_URL

    def calc(self, sender, receiver, package, tariff):
        url = f'https://tariff.pochta.ru/v2/calculate/tariff/delivery?json&object={tariff.code.code}&from={sender}&to={receiver}&weight={str(int(package.weight * 1000))}'
        response = request_func(method='GET', url=url, need_400=True, http=True)
        if response:
            return response

    def get_indexes(self, city):
        # indexes = city.zips.filter(city=city, in_calc=True)
        # if len(indexes) > 0:
        #     return indexes
        # indexes = ApiLKP().get_indexes(city.code)
        # if indexes:
        #     Zip.objects.filter(zip__in=indexes).update(in_calc=True)
            # for index in indexes:
            #     self.zip_manager.update_or_create(
            #         city=city,
            #         zip=index,
            #         defaults={'in_calc': True}
            #     )
        # else:
        #     Zip.objects.filter(city=city).update(in_calc=True)
        return Zip.objects.filter(city=city, in_calc=True)

    def calculate(self, route, package, tariff):
        sender_indexes = self.get_indexes(route.sender_city)
        receiver_indexes = self.get_indexes(route.receiver_city)
        for receiver_index in receiver_indexes:
            for sender_index in sender_indexes:
                for _ in range(3):
                    response = self.calc(tariff=tariff, sender=sender_index.zip, receiver=receiver_index.zip, package=package)
                    if response:
                        try:
                            if response.get('ground'):
                                price = response['ground']['valnds'] if tariff.direction == 'ПиП' else response['ground'][
                                    'val']
                                if price > 0 and response['delivery']['max'] == 0:
                                    # logger.error(f'No time in Pochta {response}')
                                    continue
                                return {
                                    'max_day': response['delivery']['max'],
                                    'min_day': response['delivery']['min'],
                                    'price': price / 100
                                }
                        except:
                            pass
                            # logger.error(f'Error calc Pochta. Error - {traceback.format_exc()} \n {response}')
                    if response.get('errors'):
                        error = response.get('errors')[0]
                        if str(sender_index.zip) in error['msg']:
                            sender_index.in_calc = False
                            sender_index.save()
                            break
                        elif str(receiver_index.zip) in error['msg']:
                            receiver_index.in_calc = False
                            receiver_index.save()
                            sender_indexes = Zip.objects.filter(city=route.sender_city, in_calc=True)
                            break
        return {}