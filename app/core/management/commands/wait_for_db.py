import time

from django.core.management.base import BaseCommand
from django.db import connections


class Command(BaseCommand):
    """Django command to pause execution until database is available
    """

    def handle(self, *args, **options):
        # its called when  we call wait_for_db command
        self.stdout.write('Waiting for database ...')
        db_conn = None
        while not db_conn:
            try:
                # there is gonna try to connect to the database
                db_conn = connections['default']
            except:

                self.stdout.write('Database unavailable, waiting 1 second..')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database available!'))
