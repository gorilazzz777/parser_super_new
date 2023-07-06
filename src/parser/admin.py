from django.contrib import admin
from rest_framework.authtoken.admin import TokenAdmin

from tariff_guide.models import ApiCodes
from .models import *


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('date', 'name', 'sale', 'can_add')
    list_display_links = ('date', 'name')
    search_fields = ('name', )
    list_editable = ('sale', 'can_add')


class DeliveryTariffAdmin(admin.ModelAdmin):
    list_display = ('id', 'delivery_servise', 'name', 'type', 'direction',)
    list_display_links = ('id', 'delivery_servise', 'name', 'direction',)
    search_fields = ('delivery_servise', 'name', 'type', 'direction')
    list_filter = ('delivery_servise', 'type', 'direction')

    fieldsets = (
        ('Данные Тарифа', {
            'fields': ('delivery_servise', 'name', 'code', 'type', 'direction', 'parsing_groups', 'packages',
                       'parsing_model')
        }),
    )

    # class Media:
    #     js = ['/static/parser/js/script.js', ]

    def get_fieldsets(self, request, obj=None):
        fieldsets = super(DeliveryTariffAdmin, self).get_fieldsets(request, obj)
        if request.user.is_superuser:
            fieldsets = (
                ('Данные Тарифа', {
                    'fields': ('delivery_servise', 'name', 'code', 'type', 'direction', 'parsing_groups', 'packages',
                               'limit', 'in_statistic', 'in_report', 'in_parser', 'distinct_key', 'parsing_model')
                }),
            )
        return fieldsets

    def render_change_form(self, request, context, *args, **kwargs):
        api_codes = ApiCodes.objects.all().values('serviсe_id', 'code', 'tittle')
        extra = {
            'api_codes': list(api_codes),
        }
        context.update(extra)
        return super(DeliveryTariffAdmin, self).render_change_form(request,
            context, *args, **kwargs)


class UsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'phone', 'email',)
    list_display_links = ('id', 'username', 'first_name', 'phone', 'email',)
    search_fields = ('id', 'username', 'phone', 'email')


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'report_pip', 'report_im', 'report_point',)
    list_display_links = ('id', 'user', )
    list_editable = ('report_pip', 'report_im', 'report_point',)





# admin.site.register(Users, UsersAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(DeliveryTariff, DeliveryTariffAdmin)
admin.site.register(UserProfile, UserProfileAdmin)

TokenAdmin.raw_id_fields = ['user']

