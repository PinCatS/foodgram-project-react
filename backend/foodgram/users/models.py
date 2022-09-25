from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Describe custom User model."""

    REQUIRED_FIELDS = (
        'email',
        'first_name',
        'last_name',
        'password',
    )

    first_name = models.CharField(_("first name"), max_length=150)
    last_name = models.CharField(_("last name"), max_length=150)
    email = models.EmailField(_("email address"), max_length=150)

    is_subscribed = models.BooleanField(default=False)
