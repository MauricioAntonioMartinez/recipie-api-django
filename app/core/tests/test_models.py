from unittest.mock import patch

from core.models import Ingredient, Recipe, Tag, recipe_image_file_path
from django.contrib.auth import get_user_model
from django.test import TestCase


def sample_user(email='test@test.com', password='test123'):
    return get_user_model().objects.create_user(
        email=email, password=password)


class ModelTest(TestCase):

    def test_create_user_with_email_successful(self):
        """Create a new user with the email
        """
        email = 'test@test.com'
        password = '1234567'
        user = get_user_model().objects.create_user(
            email=email, password=password)
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for the new user normalized
        """
        email = 'aaa@TTTT.COM'
        user = get_user_model().objects.create_user(
            email=email, password='12121212')
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating a user with no email
        """
        with self.assertRaises(ValueError):
            # anything should rise an error
            get_user_model().objects.create_user(None, 'test1234')

    def test_create_a_super_user(self):
        user = get_user_model().objects.create_superuser('test@test.com', '123134')
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """Test the tag string representation
        """
        tag = Tag.objects.create(
            user=sample_user(), name='Vegan')
        # test that dunder str method return the tag name

        self.assertEqual(str(tag), tag.name)

    def test_ingredient_str(self):
        """Test the ingredient string representation
        """
        ingredient = Ingredient.objects.create(
            user=sample_user(),
            name='Coco'
        )
        self.assertEqual(str(ingredient), ingredient.name)

    def test_recipe_str(self):
        """Test converting the recipe representation
        """
        recipe = Recipe.objects.create(
            user=sample_user(),
            title='Salad',
            time_minutes=5,
            price=12.0
        )
        self.assertEqual(str(recipe), recipe.title)

    @patch('uuid.uuid4')
    def test_recipe_file_name_uuid(self, mock_uuid):
        """Test that image is saved in the corrent location
        """
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid

        file_path = recipe_image_file_path(None, 'myimage.jpg')

        exp_path = f'uploads/recipe/{uuid}.jpg'

        self.assertEqual(file_path, exp_path)
