from django.contrib.auth import get_user_model
from django.test import TestCase


class ModelTest(TestCase):
    def test_create_user_with_email_successful(self):
        """Test creating a new user with the email successful
        """
        email = "test@mcuve.com"
        password = "123456"

        user = get_user_model().objects.create_user(
            email=email, password=password)
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for new user is normilzed
        """
        email = 'test@SDFSD.COM'
        user = get_user_model().objects.create_user(email, '2233433')
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error
        """
        with self.assertRaises(ValueError):
            # this should raise the value error if not this test fails
            get_user_model().objects.create_user(None, '21233')

    def test_create_new_superuser(self):
        """Test creating a new superuser
        """
        user = get_user_model().objects.create_superuser(
            "email@email.com", '232311')
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
