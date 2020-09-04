from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models


class UserManager(BaseUserManager):
    # abstract methods overwrites the defaults
    def create_user(self, email, password=None, **kargs):
        """Creates and saves new user

        Args:
            email (string): email
            password (password, optional): password. Defaults to None.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=self.normalize_email(
            email), **kargs)  # lower case the email
        user.set_password(password)  # encrypts the passsword
        user.save(using=self.db)
        return user

    def create_superuser(self, email, password):
        """Creates and saves a new superuser
        """
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self.db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead username
    """
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    # if the user is active or not
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    logout = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
