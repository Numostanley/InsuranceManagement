import uuid

from django.db import models
from django.contrib.auth.models import User
from apps.users.models import User


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    creation_date = models.DateField(auto_now=True)

    class Meta:
        abstract = True


class Category(BaseModel):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Policy(BaseModel):
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    sum_assurance = models.PositiveIntegerField()
    premium = models.PositiveIntegerField()
    tenure = models.PositiveIntegerField()
    company = models.ForeignKey("companies.Company", on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class PolicyRecord(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    policy = models.ForeignKey(Policy, on_delete=models.CASCADE)
    status = models.CharField(max_length=100, default='Pending')

    def __str__(self):
        return self.policy.name


class Question(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=500)
    comment = models.CharField(max_length=200, default='Nothing')
    asked_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.description
