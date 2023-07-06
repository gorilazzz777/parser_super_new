from django.core.management.base import BaseCommand

from app.celery import create_report_pip, create_report_im


class Command(BaseCommand):
    help = 'Создание отчетов'

    def handle(self, *args, **kwargs) -> None:
        create_report_pip.apply_async()
        create_report_im.apply_async()