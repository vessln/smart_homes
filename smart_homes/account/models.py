from django.db import models
from django.contrib.auth import models as auth_models


class CustomUserModel(auth_models.AbstractUser):

    email = models.EmailField(
        unique=True,
        null=False,
        blank=False,
    )

    def __str__(self):
        return f"User: {self.email}"


