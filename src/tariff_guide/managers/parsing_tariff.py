from django.db import models
from django.utils import timezone


class ParsingTariffClassManager(models.Manager):

    def get_parsing_tariff(self, tariff, route):
        parsing_tariff = tariff.parsing_tariffs.filter(route=route).first()
        if parsing_tariff is None:
            return self.create(tariff=tariff, route=route)
        parsing_tariff.update = timezone.now()
        parsing_tariff.save()
        return parsing_tariff