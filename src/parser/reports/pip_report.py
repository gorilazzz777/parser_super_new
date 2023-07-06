import logging

from location.models import Route, Package
from services_api.api.excel import Excel
from tariff_guide.models import Direction, ParsingGroup, ServiceCustomPackageName, ParsingTariff, DeliveryTime, Price

from .reports import ReportCreator
from ..models import DeliveryTariff

logger = logging.getLogger("app")


class PipReport(ReportCreator):

    def __init__(self):
        logger.info('Start create PIP report')
        self.direction = Direction.objects.get(code=2)
        self.bucket_folder_name = 'reports_pip'
        self.user_filter = {'userprofile__report_pip': True}
        self.subject = 'Данные по ценам доставки конкурентов ПиП'
        super().__init__(file_name=self.direction.name)

    def _ReportCreator__get_rows(self):

        groups = ParsingGroup.objects.filter(direction=self.direction, public=True)
        return Route.objects.filter(parsinggroup__in=groups).distinct()

    def update_time_headers(self, delivery_tariffs, excel):
        excel.set_value(cell=self.sheet.cell(row=1, column=3),
                        value='Сроки доставки',
                        shift=delivery_tariffs.count() * 2 - 1, fill=True)
        num = 3
        for delivery_tariff in delivery_tariffs:
            excel.set_value(cell=self.sheet.cell(row=2, column=num), value=delivery_tariff.name, shift=1, fill=True)
            excel.set_value(cell=self.sheet.cell(row=3, column=num), value='мин', fill=True)
            excel.set_value(cell=self.sheet.cell(row=3, column=num + 1), value='макс', fill=True)
            num += 2

    def update_cost_headers(self, delivery_tariffs):
        start_column = delivery_tariffs.count() * 2 + 3
        step = delivery_tariffs.count()
        for num, package in enumerate(Package.objects.filter(in_report=True)):
            fill = None
            if num % 2 == 0:
                fill = 'FFD5DA'
            excel = Excel(self.sheet, fill=fill)
            excel.set_value(cell=self.sheet.cell(row=1, column=start_column),
                            value=f'{package.weight} кг',
                            shift=delivery_tariffs.count() - 1, fill=True)
            for num, delivery_tariff in enumerate(delivery_tariffs):
                custom_package = delivery_tariff.servicecustompackagename_set.filter(package=package).first()
                if custom_package is None:
                    custom_package = ServiceCustomPackageName.objects.create(
                        package=package,
                        tariff=delivery_tariff,
                        name=package.name
                    )
                excel.set_value(cell=self.sheet.cell(row=2, column=num + start_column), value=delivery_tariff.name,
                                fill=True)
                excel.set_value(
                    cell=self.sheet.cell(row=3, column=num + start_column),
                    value=custom_package.name,
                    fill=True)
            start_column += step

    def update_template(self):
        delivery_tariffs = DeliveryTariff.objects.filter(in_report=True, direction__code=2)
        excel = Excel(self.sheet)
        self.update_time_headers(delivery_tariffs=delivery_tariffs, excel=excel)
        self.update_cost_headers(delivery_tariffs=delivery_tariffs)

    def _ReportCreator__fill_fields(self, rows):
        self.update_template()
        excel = Excel(self.sheet)
        for num, route in enumerate(rows):
            row = num + 4
            self.sheet.cell(row=row, column=1).value = route.sender_city.name
            self.sheet.cell(row=row, column=2).value = route.receiver_city.name
            tariffs = ParsingTariff.objects.filter(route=route, tariff__direction=self.direction)
            for tariff in tariffs:
                for column in range(1, self.sheet.max_column + 1):
                    if tariff.tariff.name == self.sheet.cell(row=2, column=column).value:
                        value = excel.get_value_from_merge_cells(cell=self.sheet.cell(row=1, column=column))
                        if value == 'Сроки доставки':
                            time = DeliveryTime.objects.filter(parsingtariff=tariff).first()
                            self.sheet.cell(row=row, column=column).value = time.min if time and time.min > 0 else '-'
                            self.sheet.cell(row=row,
                                            column=column + 1).value = time.max if time and time.max > 0 else '-'
                        else:
                            try:
                                weight = value.split(' ')[0]
                                custom_package = ServiceCustomPackageName.objects.filter(package__weight=weight,
                                                                                         tariff=tariff.tariff).first()
                                if custom_package and not custom_package.in_report:
                                    price = 0
                                else:
                                    price = Price.objects.filter(tariffs=tariff,
                                                                 package__weight=weight).first().price
                                self.sheet.cell(row=row, column=column).value = price if price > 0 else '-'
                            except:
                                self.sheet.cell(row=row, column=column).value = '-'
        logger.info('End create PIP report')
