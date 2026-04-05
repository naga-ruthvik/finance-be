from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    class Role(models.TextChoices):
        VIEWER = "VIEWER", "Viewer"
        ANALYST = "ANALYST", "Analyst"
        ADMIN = "ADMIN", "Admin"

    role = models.CharField(choices=Role.choices, max_length=50, default="VIEWER")
