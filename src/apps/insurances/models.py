import uuid

from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

from apps.companies.models import Company
from apps.users.models import User


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    creation_date = models.DateField(auto_now=True)

    class Meta:
        abstract = True


class Category(BaseModel):
    name = models.CharField(max_length=20)

    @staticmethod
    def get_all_categories():
        return Category.objects.order_by('name')

    @staticmethod
    def get_total_categories():
        return Company.objects.all().count()

    def __str__(self):
        return self.name


class Policy(BaseModel):
    category = models.ForeignKey(Category, related_name='policies', on_delete=models.CASCADE)
    company = models.ForeignKey(Company, related_name='policies', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    sum_assurance = models.PositiveIntegerField()
    premium = models.PositiveIntegerField()
    tenure = models.PositiveIntegerField()

    @staticmethod
    def get_all_policies():
        return Policy.objects.order_by('policy_name')

    @staticmethod
    def get_total_policies():
        return Policy.objects.all().count()

    def __str__(self):
        return self.name


class PolicyRecord(BaseModel):
    user = models.ForeignKey(User, related_name='policy_records', on_delete=models.CASCADE)
    policy = models.ForeignKey(Policy, related_name='policy_records', on_delete=models.CASCADE)
    status = models.CharField(max_length=100, default='Pending')
    date_created = models.DateField(default=now)

    @staticmethod
    def get_all_policy_records(user: User):
        return PolicyRecord.objects.filter(user=user).order_by('-date_created')

    @staticmethod
    def get_user_policy_record(user: User, id):
        try:
            return PolicyRecord.objects.filter(user=user, id=id).first()
        except PolicyRecord.DoesNotExist:
            return None

    @staticmethod
    def get_total_applied_policies():
        return PolicyRecord.objects.all().count()

    @staticmethod
    def get_total_approved_records():
        return PolicyRecord.objects.filter(status="Approved").count()

    @staticmethod
    def get_total_rejected_records():
        return PolicyRecord.objects.fitler(status="Rejected").count()

    @staticmethod
    def get_pending_records():
        return PolicyRecord.objects.filter(status="Pending").count()

    def __str__(self):
        return self.policy.name
