from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pic/customer/', null=True, blank=True)
    mobile = models.CharField(max_length=20, null=False)
    address = models.TextField()

    def __str__(self):
        return self.user.first_name
