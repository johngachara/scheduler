from django.core.management.base import BaseCommand

from scheduler.client import JobError, call


class Command(BaseCommand):
    help = "Generate this week's AI sales insight and push it to managers."

    def handle(self, *args, **options):
        try:
            result = call('/api/weekly-ai/')
        except JobError as exc:
            raise SystemExit(f'weekly insight failed: {exc}')

        if result is None:
            self.stdout.write('No sales this week. Nothing generated.')
            return

        devices = result.get('delivered_to_devices', 0)
        self.stdout.write(self.style.SUCCESS(
            f'Weekly insight generated and pushed to {devices} manager device(s).'
        ))
