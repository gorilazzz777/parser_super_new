import logging
import math

from django.utils import timezone
from location.models import Route, Package
from parser.parsers.parser import Parser
from services_api.api.LKP import ApiLKP
from services_api.api.s3_client import S3Client
from tariff_guide.models import ParsingTariff, Price, DeliveryTime

logger = logging.getLogger("app")


class TariffManager:

    def update_tariff(self, parser_price):
        self.update_calc_tariff()
        self.update_parser_tariff(parser_price=parser_price)
        todo, price = self.get_optimal_price()
        if self.update_tariff_in_calc(todo=todo, price=price):
            self.save()

    def update_calc_tariff(self):
        self.calc = ApiLKP().get_price()

    def update_parser_tariff(self, parser_price):
        self.parser = parser_price

    def get_optimal_price(self):
        if self.calc + 5 < self.parser:
            if self.parser == self.current:
                return None, None
            return 'addclienttariffs', self.parser

        if self.calc + 5 > self.parser:
            if self.current != self.calc:
                return 'removeclienttariffs', self.current
            else:
                return 'addclienttariffs', self.calc
        elif self.


    def __update_parsing_tariff(self, route, package, delivery_data):
        self.current_parsing_tariff = self.__get_parsing_tariff(route=route)
        self.__update_time_in_parsing_tariff(delivery_data=delivery_data, route=route) if package.weight == 1 else None
        old_price = self.current_parsing_tariff.prices.filter(package=package).first()
        new_price = old_price.update_price(
            price=delivery_data.get('price', 0)) if old_price else Price.manager.create_price(
            package=package,
            price=delivery_data.get('price', 0),
            tariffs=self.current_parsing_tariff
        )
        # logger.info(f'Tariff {self}\nroute {route}\npackage {package}\nprice {new_price.price}')
        if (
                new_price.package.weight != 6 and
                str(self.code.code) == '333' and
                # self.delivery_tariff_in_subscribers() and
                ((
                         old_price is None and new_price and new_price.price > 0
                 ) or
                 (
                         old_price and old_price.price != new_price.price
                 ))

        ):
            # if new_price.package.weight != 6 and str(self.delivery_tariff.code.code) == '333': if new_price and
            # new_price.price > 0: if self.delivery_tariff_in_subscribers() and: if (old_price is None and new_price
            # and new_price.price > 0) or (old_price and old_price.price != new_price.price):
            subscribers = list(set(route.parsinggroup_set.exclude(
                subscriber=None).values_list('subscriber', flat=True).distinct()))
            if subscribers:
                for subscriber in subscribers:
                    # logger.info(f'send in queue price tariff {self.delivery_tariff}')
                    S3Client(queue=subscriber).send(msg={
                        'package': package.code,
                        'sender': route.sender_city.code,
                        'receiver': route.receiver_city.code,
                        'tariff_code': self.code.code,
                        'price': new_price.price
                    })
        new_price.save()
