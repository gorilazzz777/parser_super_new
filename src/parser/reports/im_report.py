import logging
import traceback

from tariff_guide.models import Direction, ParsingTariff
from .reports import ReportCreator

logger = logging.getLogger("app")


class ImReport(ReportCreator):

    def __init__(self):
        logger.info('Start create IM report')
        self.direction = Direction.objects.get(code=1)
        self.bucket_folder_name = 'reports_im'
        self.user_filter = {'userprofile__report_im': True}
        self.subject = 'Данные по ценам доставки конкурентов ИМ'
        super().__init__(file_name=self.direction.name)

    def _ReportCreator__get_rows(self):
        return ParsingTariff.objects.filter(route__parsinggroup__public=True,
                                            tariff__direction=self.direction).distinct()

    def _ReportCreator__fill_fields(self, rows):
        for num, tariff in enumerate(rows):
            try:
                self.sheet.cell(row=num + 2, column=1).value = tariff.route.sender_city.name
                self.sheet.cell(row=num + 2, column=2).value = tariff.route.receiver_city.name
                self.sheet.cell(row=num + 2, column=3).value = tariff.route.receiver_city.region
                self.sheet.cell(row=num + 2, column=4).value = tariff.tariff.delivery_servise.name
                self.sheet.cell(row=num + 2, column=5).value = tariff.tariff.name
                self.sheet.cell(row=num + 2, column=6).value = tariff.tariff.type.name
                self.sheet.cell(row=num + 2, column=7).value = tariff.time.min if tariff.time else 0
                self.sheet.cell(row=num + 2, column=8).value = tariff.time.max if tariff.time else 0
                self.sheet.cell(row=num + 2, column=9).value = tariff.update.strftime("%d-%m-%Y, %H:%M")
                for weight, cost in enumerate(tariff.prices.filter(package__weight__gte=1).order_by('package__weight')):
                    self.sheet.cell(row=num + 2, column=weight + 10).value = cost.price
            except:
                logger.error(f'Error on create IM report. Error text {traceback.format_exc()}')
        logger.info('End create IM report')
