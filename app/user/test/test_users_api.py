from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

CREATE_USER_URL = reverse('user:create')
# this is like /api/create-user

TOKEN_URL = reverse('user:token')


def create_user(**kargs):  # helper function to create a user in the test
    return get_user_model().objects.create_user(**kargs)


# Public class testes for non authenticated api request
class PublicUserApiTest(TestCase):
    """Test the users API public
    """

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating user with valid payload is successful
        """
        payload = {
            "email": "test2@test.com",
            "password": "testcase1",
            "name": "Test name"
        }
        # sending the http request to the url create user
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        # take the data of the response
        self.assertFalse(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """Create a user that already exists
        """
        payload = {
            "email": "test@test.com",
            "password": "testcase",
            "name": "Test name"
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """The password must be more than 5 characters
        """
        payload = {
            "email": "test@test.com",
            "password": "12",
            "name": "pw"
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test that the token is created for the user
        """
        payload = {
            "email": "test@test.com",
            "password": "1212121",
        }
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)

        # checks if the key token exists in the response
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_toke_invalid_credentials(self):
        """Test that token is not created if valid credentials are given
        """
        payloadCreate = {
            "email": "test@test.com",
            "password": "1212121",
        }
        create_user(**payloadCreate)

        payload = {
            "email": "test@test.com",
            "password": "wrongpass",
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test that token is not created if the user doesn't exist
        """
        payload = {
            "email": "test@test.com",
            "password": "1212121",
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_fields(self):
        """Test that email and the password are required
        """
        res = self.client.post(TOKEN_URL, {"email": "noe", "password": ""})
        self.assertNotIn('token', res.data)
        self.assertNotEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
