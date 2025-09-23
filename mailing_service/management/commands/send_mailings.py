from django.core.management.base import BaseCommand
from mailing_service.models import Mailing


class Command(BaseCommand):
    help = 'Отправить рассылку вручную по ID'

    def add_arguments(self, parser):
        parser.add_argument('mailing_id', type=int, help='ID рассылки')

    def handle(self, *args, **kwargs):
        mailing_id = kwargs['mailing_id']
        try:
            mailing = Mailing.objects.get(pk=mailing_id)
            mailing.send()
            self.stdout.write(self.style.SUCCESS(f'Рассылка #{mailing_id} успешно отправлена.'))
        except Mailing.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Рассылка с ID {mailing_id} не найдена.'))