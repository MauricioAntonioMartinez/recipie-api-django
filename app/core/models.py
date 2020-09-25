import os
import uuid

from django.conf import settings  # this is how we can retrive variables
# for the settings file
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models

# Maneger User class is the class that provides the creation
# of user or admin and all methods out of the box


def recipe_image_file_path(instance, file_name):
    """Generate file path for new recipe image

    Args:
        instance : instance of the current session
        file_name (str): file name with the extension
    """
    ext = file_name.split('.')[-1]  # the last item
    filename = f'{uuid.uuid4()}.{ext}'
    return os.path.join('uploads/recipe/', filename)


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **kargs):
        """Creates and saves a new user

        Args:
            email ([type]): [description]
            password ([type], optional): [description]. Defaults to None.
        """
        if not email:
            raise ValueError('User Must Have An Email Address')
        new_email = self.normalize_email(email)
        user = self.model(email=new_email, **kargs)
        # this is the same as creating a user model
        user.set_password(password)  # this incrypt the password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        # create a normal user
        user = self.create_user(email=email, password=password)
        user.is_staff = True
        user.is_superuser = True  # adding the fields of a superuser
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):  # this classes provides
    # all the free functionality out of the box that django provides
    # with this we can customize
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = UserManager()
    USERNAME_FIELD = 'email'


class Tag(models.Model):
    """Tag to be used for a recipie
    """
    name = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Ingredient to be used in a recipe
    """
    name = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Recipe object
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)
    ingredients = models.ManyToManyField(Ingredient)
    tags = models.ManyToManyField(Tag)
    image = models.ImageField(null=True, upload_to=recipe_image_file_path)
    # pass the reference to the function so when its saved this will call and retrieve
    # the path, this pass the instance as well

    def __str__(self):
        return self.title
