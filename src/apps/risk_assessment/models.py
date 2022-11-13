from django.db import models

from apps.insurances.models import BaseModel, Policy
from apps.users.models import User


class RiskAssessment(BaseModel):
    policy = models.ForeignKey(Policy, on_delete=models.CASCADE, related_name="policy")
    assessment = models.TextField()
    risk_level = models.CharField(max_length=100)
    assessor = models.ForeignKey(User, on_delete=models.CASCADE, )
    type = models.CharField(max_length=100)
