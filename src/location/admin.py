from django.contrib import admin
from django.contrib.admin import TabularInline, SimpleListFilter

from .models import *


class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'region', 'code', 'kladr', 'dpd_code', 'cdek_code',)
    list_display_links = ('id',)
    search_fields = ('name', 'region', 'code', 'kladr', 'dpd_code', 'cdek_code',)
    list_editable = ('name', 'region', 'code', 'kladr', 'dpd_code', 'cdek_code',)


class ParsingGroupInline(TabularInline):
    model = Route.parsinggroup_set.through
    extra = 0
    verbose_name = 'Группа парсинга'
    verbose_name_plural = 'Группы парсинга'


class SenderCityFilter(SimpleListFilter):
    title = 'Город отправитель'
    parameter_name = 'sender_city'

    def lookups(self, request, model_admin):
        return [(city.id, f'{city.name} ({city.region})') for city in City.objects.filter(delivery_lap=True)]

    def queryset(self, request, queryset):
        if self.used_parameters.get('sender_city'):
            return queryset.filter(sender_city_id=self.used_parameters['sender_city'])
        return queryset


class ReceiverCityFilter(SimpleListFilter):
    title = 'Город получатель'
    parameter_name = 'receiver_city'

    def lookups(self, request, model_admin):
        return [(city.id, f'{city.name} ({city.region})') for city in City.objects.filter(delivery_lap=True)]

    def queryset(self, request, queryset):
        if self.used_parameters.get('receiver_city'):
            return queryset.filter(receiver_city_id=self.used_parameters['receiver_city'])
        return queryset


class RouteAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender_city', 'receiver_city', 'zone',)
    list_display_links = ('id', 'sender_city', 'receiver_city', 'zone')
    search_fields = ('sender_city', 'receiver_city', )
    list_filter = ('zone__code', SenderCityFilter, ReceiverCityFilter,)

    list_per_page = 6

    inlines = [ParsingGroupInline]


class SberPackageInline(admin.TabularInline):
    model = DeliveryServicePackage
    extra = 0
    can_delete = False
    verbose_name = 'Упаковка Сберлогистики'
    verbose_name_plural = 'Упковки Сберлогистики'


class PackageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'height', 'depth', 'width', 'weight', )
    list_display_links = ('id', 'name', 'height', 'depth', 'width', 'weight', )
    list_filter = ('pip',)

    # inlines = [SberPackageInline]


    fieldsets = (
        ('Основные данные', {
            'fields': ('name', 'height', 'depth', 'width', 'weight', 'pip')
        }),
        ('Данные по для парсинга', {
            'fields': ('dpd_shop_name', 'pony_express_name', 'cdek_box_name', 'value', 'sberlogistic_package',
                       'cdek_box_package')
        })
    )


class DeliveryServicePackageAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'get_delivery_tariff', )
    list_display_links = ('code', 'name', 'get_delivery_tariff',)

    def get_delivery_tariff(self, obj):
        return obj.delivery_tariff.name


admin.site.register(Package, PackageAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(DeliveryServicePackage, DeliveryServicePackageAdmin)
admin.site.register(Route, RouteAdmin)
