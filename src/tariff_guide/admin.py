import threading

from django.contrib.admin import SimpleListFilter, ModelAdmin, TabularInline, site, action
from django.db.models import QuerySet
from django.forms import ModelForm
from django.utils.safestring import mark_safe

from location.models import DeliveryType, Zone
from parser.models import DeliveryTariff, Service
from .models import *


class ServiceCustomPackageNameAdmin(ModelAdmin):
    list_display = ('id', 'package', 'tariff', 'name', 'in_report',)
    list_display_links = ('id', 'package', 'tariff', 'name', )
    list_editable = ('in_report',)


class ApiCodesAdmin(ModelAdmin):
    list_display = ('id', 'serviсe', 'code', 'tittle', 'direction')
    list_display_links = ('id', 'serviсe')
    search_fields = ('serviсe', 'code', 'tittle')
    list_editable = ('code', 'tittle', 'direction')


class ScriptAdmin(ModelAdmin):
    list_display = ('id', 'name', 'description')
    list_display_links = ('id', 'name', 'description')


class DirectionAdmin(ModelAdmin):

    list_display = ('name',)


class RoutesInline(TabularInline):
    model = ParsingGroup.routes.through
    extra = 0
    verbose_name = 'Маршрут'
    verbose_name_plural = 'Маршруты'


class TariffInline(TabularInline):
    model = ParsingGroup.deliverytariff_set.through
    extra = 0
    verbose_name = 'Тариф на доставку'
    verbose_name_plural = 'Тарифы на доставку'


class ParsingGroupAdmin(ModelAdmin):
    list_display = ('name', 'script', 'direction')
    list_display_links = ('name', 'script', 'direction')

    readonly_fields = ('routes_list', 'routes')

    inlines = [TariffInline]

    fieldsets = (
        ('Общее', {
            'fields': ('name', ('script', 'direction'), )
        }),
    )

    def get_fieldsets(self, request, obj=None):
        fieldsets = super(ParsingGroupAdmin, self).get_fieldsets(request, obj)
        if obj and obj.script:
            if obj.script.code in [1, 2, 3]:
                fieldsets += (
                    ('Города', {
                        'fields': ('city',)
                    }),
                )
            if obj.script.code == 5:
                fieldsets += (
                    ('Маршруты', {
                        'fields': ('routes',)
                    }),
                )
        return fieldsets

    def routes_list(self, obj):
        return obj.routes.all()

    def save_model(self, request, obj, form, change):
        res = super().save_model(request, obj, form, change)
        thread = threading.Thread(target=Route.manager.update_routes_for_group, args=(obj, ))
        thread.start()
        return res


class ZoneFilter(SimpleListFilter):
    title = 'Зона'
    parameter_name = 'zone_filter'
    placeholder = 'Фильтр по зоне'

    def lookups(self, request, model_admin):
        return [(zone.id, f'{zone.code}') for zone in Zone.objects.all()]

    def queryset(self, request, queryset):
        if self.used_parameters.get('zone_filter'):
            return queryset.filter(route__zone__id=self.used_parameters['zone_filter'])
        return queryset


class SenderCityFilter(SimpleListFilter):
    title = 'Город отправитель'
    parameter_name = 'sender_city'

    def lookups(self, request, model_admin):
        return [(city.id, f'{city.name} ({city.region})') for city in City.objects.filter(courier_delivery=True)]

    def queryset(self, request, queryset):
        if self.used_parameters.get('sender_city'):
            return queryset.filter(route__sender_city_id=self.used_parameters['sender_city'])
        return queryset


class ReceiverCityFilter(SimpleListFilter):
    title = 'Город получатель'
    parameter_name = 'receiver_city'

    def lookups(self, request, model_admin):
        return [(city.id, f'{city.name} ({city.region})') for city in City.objects.filter(courier_delivery=True)]

    def queryset(self, request, queryset):
        if self.used_parameters.get('receiver_city'):
            return queryset.filter(route__receiver_city_id=self.used_parameters['receiver_city'])
        return queryset


class TariffFilter(SimpleListFilter):
    title = 'Тариф на доставку' # or use _('country') for translated title
    parameter_name = 'tariff'

    def lookups(self, request, model_admin):
        return [(tariff.id, f'{tariff.name} ({tariff.direction.name})') for tariff in DeliveryTariff.objects.all()]

    def queryset(self, request, queryset):
        if self.used_parameters.get('tariff'):
            return queryset.filter(tariff_id=self.used_parameters['tariff'])
        return queryset


class DeliveryServiceFilter(SimpleListFilter):
    title = 'Служба доставки' # or use _('country') for translated title
    parameter_name = 'delivery_service'

    def lookups(self, request, model_admin):
        return [(service.id, f'{service.name}') for service in Service.objects.all()]

    def queryset(self, request, queryset):
        if self.used_parameters.get('delivery_service'):
            return queryset.filter(tariff__delivery_servise_id=self.used_parameters['delivery_service'])
        return queryset


class DeliveryTypeFilter(SimpleListFilter):
    title = 'Тип доставки' # or use _('country') for translated title
    parameter_name = 'type'

    def lookups(self, request, model_admin):
        return [(t.id, f'{t.name}') for t in DeliveryType.objects.all()]

    def queryset(self, request, queryset):
        if self.used_parameters.get('type'):
            return queryset.filter(tariff__type_id=self.used_parameters['type'])
        return queryset


class PriceInline(TabularInline):
    model = Price
    extra = 0
    can_delete = False
    verbose_name = 'Стоимости'
    verbose_name_plural = 'Стоимость'


class ParsingTariffAdmin(ModelAdmin):
    list_display = ('update', 'sender_city', 'receiver_city', 'zone', 'tariff', 'delivery_service',
                    'delivery_type', 'min', 'max', 'prices',)
    list_display_links = ('update', 'sender_city', 'receiver_city', 'zone', 'tariff', 'delivery_service',
                    'delivery_type', 'min', 'max', 'prices',)
    list_filter = (SenderCityFilter, ReceiverCityFilter, ZoneFilter, TariffFilter, DeliveryServiceFilter,
                   DeliveryTypeFilter, 'tariff__direction')

    readonly_fields = ('route', 'time')

    fieldsets = (
        ('Общее', {
            'fields': ('update', 'tariff', 'route',)
        }),
        ('Сроки доставки', {
            'fields': ('is_fast', 'is_slowest', 'time', )
        })
    )

    actions = ['update']

    list_per_page = 4

    inlines = [PriceInline]

    @action(description='Обновить цены')
    def update(self, request, qs: QuerySet):
        for tariff in qs:
            thread = threading.Thread(target=tariff.tariff.update_tariffs, args=(tariff.route, ))
            thread.start()
        self.message_user(request=request,
                            message=f'Отправлена задача на обновление тарифов')

    def sender_city(self, obj):
        return obj.route.sender_city

    def prices(self, obj):
        head = ''
        body = ''
        for p in obj.prices.all():
            head += f'<th  scope="col">{p.package.weight} кг</th>'
            body += f'<td scope="row">{p.price}</td>'
        s = mark_safe(f'''
        <table class="table">
            <thead>
                <tr style="font-size: 10px">
                    {head}
                </tr>
            </thead>
            <tbody>
                <tr style="font-size: 10px">
                    {body}
                </tr>
            </tbody>
        </table>
        ''')
        return s

    def receiver_city(self, obj):
        return obj.route.receiver_city

    def zone(self, obj):
        return obj.route.zone.code if obj.route.zone else '---'

    def delivery_service(self, obj):
        return obj.tariff.delivery_servise.name

    def delivery_type(self, obj):
        return obj.tariff.type.name

    def max(self, obj):
        return obj.time.max if obj.time else 0

    def min(self, obj):
        return obj.time.min if obj.time else 0

    sender_city.short_description = 'Город отправитель'
    prices.short_description = 'Цены доставки'
    receiver_city.short_description = 'Город получатель'
    zone.short_description = 'Зона'
    delivery_type.short_description = 'ДТип доставки'
    max.short_description = 'Макс. срок'
    min.short_description = 'Мин. срок'


site.register(Script, ScriptAdmin)
site.register(ServiceCustomPackageName, ServiceCustomPackageNameAdmin)
site.register(ApiCodes, ApiCodesAdmin)
site.register(Direction, DirectionAdmin)
site.register(ParsingGroup, ParsingGroupAdmin)
site.register(ParsingTariff, ParsingTariffAdmin)
site.register(ParsingModels)