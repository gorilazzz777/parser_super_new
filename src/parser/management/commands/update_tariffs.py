from django.core.management.base import BaseCommand

from app.tasks import update_tariffs


class Command(BaseCommand):
    help = 'обновление тарифов'

    def handle(self, *args, **kwargs) -> None:
        update_tariffs.apply_async()