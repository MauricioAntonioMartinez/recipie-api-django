import time

from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError


class Command(BaseCommand):
    """Django commnad to pause execution until database is avalable
    """

    def handle(self, *args, **options):
        self.stdout.write('WAITING FOR DATABASE ...')
        db_conn = None

        while not db_conn:
            try:
                db_conn = connections['default']
            except OperationalError:
                self.stdout.write('DATABASE UNAVAILABLE WAITING 1 SECOND')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('CONNECTED WITH THE DATABASE'))
