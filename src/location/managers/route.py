from django.db import models

from parser.helpers import query_debugger


class RouteClassManager(models.Manager):

    def _get_receivers_for_script(self, city, group):
        from location.models import City

        if group.script.code == 1:
            return group.city.all()
        elif group.script.code == 2:
            return City.objects.filter(delivery_lap=True)
        elif group.script.code == 3:
            return City.objects.filter(delivery_lap=True, region=city.region)

    def update_routes_for_group(self, group):
        group.routes.clear()
        senders = group.city.all()
        for s_num, sender in enumerate(senders):
            receivers = self._get_receivers_for_script(sender, group)
            for r_num, receiver in enumerate(receivers):
                route, created = self.get_or_create(
                    sender_city=sender,
                    receiver_city=receiver
                )
                group.routes.add(route)

    def get_queryset(self):
        return RouteQuerySet(self.model)

    def get_routes(self, groups):
        return self.get_queryset().get_routes(groups=groups)

    def get_routes_for_parse(self, tariff, limit):
        routes_ids = tariff.parsing_tariffs.filter(
            route__parsinggroup__in=tariff.parsing_groups.all()
        ).order_by('update').values_list('route', flat=True).distinct()[:limit]
        return self.filter(id__in=routes_ids)

    def without_tariff(self, tariff):
        return self.get_queryset().without_tariff(tariff=tariff).select_related('sender_city', 'receiver_city')


class RouteQuerySet(models.QuerySet):

    def without_tariff(self, tariff):
        return self.exclude(parsingtariff__tariff=tariff).select_related('sender_city', 'receiver_city')

    def get_routes(self, groups):
        return self.filter(parsinggroup__in=groups).order_by('parsingtariff__update').distinct()