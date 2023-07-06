from django.db import models


class DeliveryTimeManager:
    def update_time(self, data, route):
        need_set_rating = False
        if self.min != int(data.get('min_day', 0)):
            self.min = int(data.get('min_day', 0))
            need_set_rating = True
        if self.max != int(data.get('max_day', 0)):
            self.max = int(data.get('max_day', 0))
            need_set_rating = True
        if need_set_rating:
            self.save()
            # self.set_rating(route=route)

    def set_rating(self, route):
        self.cheaper.clear()
        self.more_expensive.clear()
        cheapers = DeliveryTimeClassManager().filter_i(max=3)
        # cheapers = DeliveryTimeClassManager().filter(min__lte=self.min, parsing_tariff__route=route).exclude(id=self.id)
        # more_expensivs = DeliveryTimeClassManager().filter(max__gte=self.max, parsing_tariff__route=route).exclude(id=self.id)
        # if len(cheapers) == len(more_expensivs) == 0:
        #     return
        # for cheaper in cheapers:
        #     self.cheaper.add(cheaper.parsing_tariff.tariff)
        # for more_expensive in more_expensivs:
        #     self.more_expensive.add(more_expensive.parsing_tariff.tariff)


class DeliveryTimeClassManager(models.Manager):

    def create_time(self, current_route, *args, **kwargs):
        price = self.create(*args, **kwargs)
        # price.set_rating(current_route)
        return price

    def filter_i(self, *args, **kwargs):
        return self.filter(*args, *kwargs)