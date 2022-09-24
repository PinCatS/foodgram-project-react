from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Describe custom User model."""

    is_subscribed = models.BooleanField(default=False)
