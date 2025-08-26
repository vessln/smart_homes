from django.db import models
from django.contrib.auth import models as auth_models


class CustomUserModel(auth_models.AbstractUser):
    MAX_USERNAME_LENGTH = 20

    username = models.CharField(
        max_length=MAX_USERNAME_LENGTH,
        unique=True,
        null=False,
        blank=False,
    )

    email = models.EmailField(
        unique=True,
        null=False,
        blank=False,
    )

    def __str__(self):
        return f"User: {self.email}"


