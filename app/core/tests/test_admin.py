from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self):
        """Creates a super user in the client and log ins
        """
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email="test@tes.com", password='123123')
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='some@some.com', password='Some Pass', name='Some Name')

    def test_users_listed(self):
        """Test that users are listed on user page
        """
        url = reverse('admin:core_user_changelist')
        # for the endpoint named like that
        res = self.client.get(url)
        self.assertContains(res, self.user.name)
        # inteligent look for this objects
        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        """Test that the user edit works
        """
        url = reverse('admin:core_user_change', args=[self.user.id])
        # endpoint to change the a user
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test that the create user works
        """
        url = reverse('admin:core_user_add')
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
