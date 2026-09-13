from django.core.management.base import BaseCommand

from scheduler.client import JobError, call


class Command(BaseCommand):
    help = "Generate yesterday's AI sales insight and push it to managers."

    def handle(self, *args, **options):
        try:
            result = call('/api/daily-ai/')
        except JobError as exc:
            raise SystemExit(f'daily insight failed: {exc}')

        if result is None:
            self.stdout.write('No sales yesterday. Nothing generated.')
            return

        devices = result.get('delivered_to_devices', 0)
        self.stdout.write(self.style.SUCCESS(
            f'Daily insight generated and pushed to {devices} manager device(s).'
        ))
