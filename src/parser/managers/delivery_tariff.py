import logging
import math

from django.utils import timezone
from location.models import Route, Package
from parser.parsers.parser import Parser
from services_api.api.s3_client import S3Client
from tariff_guide.models import ParsingTariff, Price, DeliveryTime

logger = logging.getLogger("app")


class DeliveryTariffManager:
    def __init__(self):
        self.packages_for_parse = self.__packages_for_parse()
        self.current_parsing_tariff = None

    def update_tariffs(self, route=None):
        start = timezone.now()
        routes = []
        if self.parsing_model:
            parser_model = getattr(Parser(), self.parsing_model.code)
            if parser_model and self.packages_for_parse:
                routes = self.get_routes_for_parse(route=route)
                for num, route in enumerate(routes):
                    for try_count in range(5):
                        for package in self.packages_for_parse:
                            delivery_data = parser_model.calculate(route=route, package=package, tariff=self)
                            packages = self.__get_packages_for_update(package)
                            for update_package in packages:
                                self.__update_parsing_tariff(route=route, package=update_package,
                                                             delivery_data=delivery_data)
                        if self.__check_for_zero_price():
                            break
            else:
                print(f'NO parser model - {parser_model} or no packages - {self.packages_for_parse}')
        else:
            print('NO SELF PARSING MODEL!')
        return {
                'tariff': self.name,
                'direction': self.direction.name,
                'routes': len(routes),
                'time': str(timezone.now() - start),
                'parsing_model': self.parsing_model.code
            }

    def __check_for_zero_price(self):
        prices = self.current_parsing_tariff.prices.all()
        if prices.count() == prices.filter(price=0).count():
            return True
        elif prices.count() == prices.filter(price__gt=0).count():
            return True

    def get_routes_for_parse(self, route=None):
        if route:
            return[route]
        routes_in_groups = Route.manager.get_routes(groups=self.parsing_groups.all())
        limit = math.ceil(routes_in_groups.count() / (7 * 24))
        routes_no_parsed = routes_in_groups.without_tariff(tariff=self)
        if routes_no_parsed:
            return routes_no_parsed[:limit]
        return Route.manager.get_routes_for_parse(tariff=self, limit=limit)

    def __packages_for_parse(self):
        return Package.manager.get_package_for_parse(tariff=self)

    def __get_packages_for_update(self, package):
        if self.distinct_key:
            return Package.manager.get_packages_for_update(tariff=self, package=package)
        return [package]

    def __get_parsing_tariff(self, route):
        return ParsingTariff.manager.get_parsing_tariff(tariff=self, route=route)

    def __update_time_in_parsing_tariff(self, delivery_data, route):
        if self.current_parsing_tariff.time:
            return self.current_parsing_tariff.time.update_time(data=delivery_data, route=route)
        self.current_parsing_tariff.time = DeliveryTime.manager.create_time(
            current_route=route,
            min=delivery_data.get('min_day', 0),
            max=delivery_data.get('max_day', 0)
        )
        self.current_parsing_tariff.save()

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
