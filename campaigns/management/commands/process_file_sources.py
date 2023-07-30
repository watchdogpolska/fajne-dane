from django.core.management.base import BaseCommand

from campaigns.models import FileSource
from campaigns.models.consts import FileSourceStatus


class Command(BaseCommand):
    help = "Processes all unprocessed FileSources"


    def handle(self, *args, **options):
        if FileSource.objects.filter(status=FileSourceStatus.PROCESSING).first():
            self.stdout.write(
                self.style.HTTP_INFO('Other command is still running. Skipping.')
            )
            return

        pending = FileSource.objects.filter(status=FileSourceStatus.CREATED)
        self.stdout.write(
            self.style.HTTP_INFO(f'Found {pending.count()} pending FileSources.')
        )
        for source in pending:
            self.stdout.write(
                self.style.HTTP_INFO(f'Started processing {source.id!r}')
            )
            source.process()
            self.stdout.write(
                self.style.SUCCESS(f'Successfully processed {source.id!r}')
            )
