from django.db import models


class PackageClassManager(models.Manager):

    def get_queryset(self):
        return PackageQuerySet(self.model)

    def get_package_for_parse(self, tariff):
        return self.get_queryset().get_package_for_parse(tariff=tariff)

    def get_packages_for_update(self, tariff, package):
        return self.get_queryset().get_packages_for_update(tariff, package)


class PackageQuerySet(models.QuerySet):

    def get_packages_for_update(self, tariff, package):
        return self.filter(**{tariff.distinct_key: getattr(package, tariff.distinct_key)})

    def get_package_for_parse(self, tariff):
        if tariff.distinct_key:
            return self.__distinct(key=tariff.distinct_key)
        if tariff.id:
            return tariff.packages.all()

    def __distinct(self, key):
        packages = list(set(self.exclude(**{key: None}).values_list(key, flat=True).distinct()))
        packages_ids = [self.filter(**{key: package_code}).last().id for package_code in packages]
        return self.filter(id__in=packages_ids)