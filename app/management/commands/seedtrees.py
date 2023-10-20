import time

from django.core.management.base import BaseCommand

from app.helpers.seed_data import process, create_hierarchy


class Command(BaseCommand):
    help = 'Seed test data to database'

    def handle(self, *args, **options):
        process_started = time.time()
        process()
        process_finished = time.time()
        self.stdout.write(self.style.SUCCESS(
            'Database successfully populated with primary data'
            f'in {process_finished - process_started} seconds.\n'
            'Hierarchy creation started...'
        ))
        create_hierarchy_started = time.time()
        create_hierarchy()
        create_hierarchy_finished = time.time()
        self.stdout.write(self.style.SUCCESS(
            f'Hierarchical relations successfully created in {create_hierarchy_finished - create_hierarchy_started} seconds'
        ))
