from location.services.points import ManagePoints

from .reports import ReportCreator


class TerminalsReport(ReportCreator):

    def __init__(self):
        self.bucket_folder_name = 'reports_terminals'
        self.user_filter = {'userprofile__report_point': True}
        self.subject = 'Данные ПВЗ конкурентов'
        super().__init__(file_name='ПВЗ')

    def _ReportCreator__get_rows(self):
        return ManagePoints().filter(active=True)

    def _ReportCreator__fill_fields(self, rows):
        for num, point in enumerate(rows):
            row = num + 2
            self.sheet.cell(row=row, column=1).value = point.delivery_service.name
            self.sheet.cell(row=row, column=2).value = point.courier
            self.sheet.cell(row=row, column=3).value = point.city.name
            self.sheet.cell(row=row, column=4).value = point.city.region
            self.sheet.cell(row=row, column=4).value = point.address
            self.sheet.cell(row=row, column=5).value = '+' if point.reception_lap else '-'
            self.sheet.cell(row=row, column=6).value = '+' if point.delivery_lap else '-'
            self.sheet.cell(row=row, column=7).value = point.type.name
