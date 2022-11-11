import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser, Group, UserManager


# Create your models here.

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4())
    email = models.EmailField(max_length=254, unique=True)
    username = models.CharField(
        max_length=254, null=True, blank=True, unique=True
    )
    image = models.ImageField(upload_to='uploads/profile_pictures')
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    phone_number = models.CharField(max_length=254, null=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=255, null=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="user_group", null=True, default=None)
    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["email"]

    @property
    def get_name(self):
        return self.first_name + " " + self.last_name
