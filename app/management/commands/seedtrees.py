from django.core.management.base import BaseCommand
from app.helpers.seed_data import process, create_hierarchy


class Command(BaseCommand):
    help = 'Seed data to database'

    def handle(self, *args, **options):
        process()
        create_hierarchy()
        self.stdout.write(self.style.SUCCESS('Database successfully populated with data'))