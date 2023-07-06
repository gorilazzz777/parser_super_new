from abc import ABC, abstractmethod
from datetime import datetime, timedelta

import pytz
from django.contrib.auth.models import User

from app.settings import PATH_TO_RESULT_REPORTS, PATH_TO_TEMPLATES_REPORTS
from openpyxl import load_workbook
from services_api.api.s3_client import S3Client

from services_api.api.send_mail import MailSender


class ReportCreator(ABC):
    def __init__(self, file_name=None):
        if file_name:
            self.file_name = file_name
            self.wb = load_workbook(f'{PATH_TO_TEMPLATES_REPORTS}{self.file_name}.xlsx')
            self.sheet = self.wb.active
        else:
            self.file_name = None

    @abstractmethod
    def __get_rows(self):
        pass

    @abstractmethod
    def __fill_fields(self, rows):
        pass

    def get_name_current_month(self):
        month = {
            1: 'Январь',
            2: 'Февраль',
            3: 'Март',
            4: 'Апрель',
            5: 'Май',
            6: 'Июнь',
            7: 'Июль',
            8: 'Август',
            9: 'Сентябрь',
            10: 'Октябрь',
            11: 'Ноябрь',
            12: 'Декабрь',
        }
        stop = datetime.now(pytz.timezone('Europe/Moscow')) - timedelta(days=1)
        start = pytz.utc.localize(datetime(stop.year, stop.month, 1))
        return month[start.month]

    def save_file(self):
        self.wb.save(f'{PATH_TO_RESULT_REPORTS}{self.file_name}.xlsx')

    def create_report(self):
        rows = self.__get_rows()
        table = self.__fill_fields(rows)
        if self.file_name:
            self.save_file()
        else:
            return table
        self.upload_report_to_s3()

    def upload_report_to_s3(self):
        S3Client().push_file(file_name=self.file_name, folder_name=self.bucket_folder_name, upload_file_name=self.get_name_current_month())

    def send_report(self):
        for user in User.objects.filter(**self.user_filter):
            if user.email:
                MailSender().send_email(addr_to=user.email, files=[f'{PATH_TO_RESULT_REPORTS}{self.file_name}.xlsx'], subject=self.subject)
