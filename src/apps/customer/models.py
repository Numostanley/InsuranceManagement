from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pic/Customer/', null=True, blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20, null=False)

    @property
    def get_name(self):
        return f'{self.user} {self.user}'

    def __str__(self):
        return self.user
