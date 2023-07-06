import traceback

from django.db import models


class PriceManager:
    def update_price(self, price):
        if self.price != price:
            self.price = price
            self.set_rating()
            self.save()
        return self

    def set_rating(self):
        from tariff_guide.models import Price

        self.cheaper.clear()
        self.more_expensive.clear()
        prices = Price.manager.filter(tariffs__route=self.tariffs.route, package=self.package,
                             tariffs__tariff__direction=self.tariffs.tariff.direction,
                             price__gt=0).exclude(id=self.id)

        cheapers = prices.filter(price__lte=self.price)
        more_expensivs = prices.filter(price__gte=self.price)
        if len(cheapers) == len(more_expensivs) == 0:
            return
        for cheaper in cheapers:
            self.cheaper.add(cheaper.tariffs.tariff)
        for more_expensive in more_expensivs:
            self.more_expensive.add(more_expensive.tariffs.tariff)


class PriceClassManager(models.Manager):

    def create_price(self, *args, **kwargs):
        try:
            price = self.create(*args, **kwargs)
            # price.set_raiting()
            return price
        except:
            print(traceback.format_exc())