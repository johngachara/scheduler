from django.core.management.base import BaseCommand

from scheduler.client import JobError, call


class Command(BaseCommand):
    help = "Email the sales report for completed sales that have not been reported yet."

    def handle(self, *args, **options):
        try:
            result = call('/api/send_sale2')
        except JobError as exc:
            # Non-zero exit, so cron's mail and the container's status both
            # show the failure instead of it being buried in a log file.
            raise SystemExit(f'sales report failed: {exc}')

        if result is None:
            self.stdout.write('No unreported sales. Nothing sent.')
        else:
            self.stdout.write(self.style.SUCCESS('Sales report sent.'))
