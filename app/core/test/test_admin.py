from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse


class AdminSiteTest(TestCase):
    def setUp(self):  # called before every test
        self.client = Client()  # overwrite client variable
        self.admin_user = get_user_model().objects.create_superuser(
            email="admin@admin.com", password="123344")
        self.client.force_login(self.admin_user)  # logs the user
        self.user = get_user_model().objects.create_user(
            email="test@test.com", password="1234",
            name="Some Name")

    def test_users_listed(self):
        """Test that users are listed on user page
        """  # define in django docs
        url = reverse(
            "admin:core_user_changelist")  # generate url for our list user
        response = self.client.get(url)
        # http response contains the email
        self.assertContains(response, self.user.name)
        self.assertContains(response, self.user.email)

    def test_user_page_change(self):
        """Test that user edit page works
        """
        url = reverse('admin:core_user_change', args=[self.user.id])
        # /admin/core/user/1
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_page_user_page(self):
        """Test that the create user page works
        """
        url = reverse(
            'admin:core_user_add')  # this pages are defined by django
        # to manage the creations login of the admins and users
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
