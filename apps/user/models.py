from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from apps.core.models import TimeStampedModel
from django.utils.translation import gettext_lazy as _


class UserAccountManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser, TimeStampedModel):
    USER_TYPE_CHOICES = (
        ("admin", 'Admin'),
        ("member", 'Member'),
    )

    # Removing the username field
    username = None
    user_type = models.CharField(max_length=25, choices=USER_TYPE_CHOICES, null=True, blank=True, default="member")
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserAccountManager()

    def __str__(self):
        return str(self.email)

    def get_user_type(self):
        return self.user_type

    def set_password(self, raw_password):
        if raw_password:
            super().set_password(raw_password)
        else:
            self.password = None

    def save(self, *args, **kwargs):
        if not self.password:
            self.set_unusable_password()
        super().save(*args, **kwargs)
