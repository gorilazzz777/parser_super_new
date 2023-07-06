from django.db import models

from location.models import Route


class ParsingGroupClassManager(models.Manager):
    def get_queryset(self):
        return ParsingGroupQuerySet(self.model)

    def in_report(self):
        return self.get_queryset().in_report()


class ParsingGroupQuerySet(models.QuerySet):

    def in_report(self):
        return self.filter(in_report=True)