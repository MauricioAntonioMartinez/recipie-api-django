from unittest.mock import patch

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase


class CommandTests(TestCase):

    def test_wait_for_db_ready(self):
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.return_value = True
            call_command('wait_for_db')  # the commando to connect to the db
            # that we will create
            self.assertEqual(gi.call_count, 1)

    @patch('time.sleep', return_value=True)  # to not wait and runs direct
    def test_wait_for_db(self, ts):
        """Test waiting for db
        """
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.side_effect = [OperationalError] * \
                5 + [True]  # 5 times will raise
            # the operational error
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 6)
