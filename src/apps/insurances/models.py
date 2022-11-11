from django.db import models
from django.utils.timezone import now

from apps.users.models import User


class Category(models.Model):
    name = models.CharField(max_length=20)
    date_created = models.DateField(auto_now=True)

    @staticmethod
    def get_all_categories():
        return Category.objects.order_by('name')

    def __str__(self):
        return self.name


class Policy(models.Model):
    category = models.ForeignKey(Category, related_name='policies', on_delete=models.CASCADE)
    policy_name = models.CharField(max_length=200)
    sum_assurance = models.PositiveIntegerField()
    premium = models.PositiveIntegerField()
    tenure = models.PositiveIntegerField()
    date_created = models.DateField(auto_now=True)

    @staticmethod
    def get_all_policies():
        return Policy.objects.order_by('policy_name')

    def __str__(self):
        return self.policy_name


class PolicyRecord(models.Model):
    user = models.ForeignKey(User, related_name='policy_records', on_delete=models.CASCADE)
    policy = models.ForeignKey(Policy, related_name='policy_records', on_delete=models.CASCADE)
    status = models.CharField(max_length=100, default='pending')
    date_created = models.DateField(auto_now=True)

    @staticmethod
    def get_all_policy_records(user: User):
        return PolicyRecord.objects.filter(user=user).order_by('-date_created')

    @staticmethod
    def get_user_policy_record(user: User, id):
        try:
            return PolicyRecord.objects.filter(user=user, id=id).first()
        except PolicyRecord.DoesNotExist:
            return None

    def __str__(self):
        return self.policy


class Question(models.Model):
    customer = models.ForeignKey(User, related_name='questions', on_delete=models.CASCADE)
    description = models.TextField()
    admin_comment = models.TextField()
    date_created = models.DateField(default=now)

    def __str__(self):
        return self.description
