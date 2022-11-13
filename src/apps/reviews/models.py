from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _

from apps.companies.models import Company
from apps.users.models import User


class Review(models.Model):
    company = models.ForeignKey(Company,
                                related_name='reviews',
                                on_delete=models.CASCADE)
    reviewer = models.ForeignKey(User,
                             related_name='reviews',
                             on_delete=models.SET_NULL,
                             null=True,
                             blank=True)
    rating = models.IntegerField(_('rating'),
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(_('comment'), blank=True)
    date_created = models.DateTimeField(_('date created'), auto_now_add=True)

    class Meta:
        ordering = ['-date_created']
        constraints = [
            models.UniqueConstraint(name="const", fields=['company', 'reviewer'])
        ]

    @staticmethod
    def create_review(company: Company, reviewer: User, rating: int, comment: str or None):
        if comment:
            return Review.objects.create(
                company=company,
                reviewer=reviewer,
                rating=rating,
                comment=comment
            )
        return Review.objects.create(
            company=company,
            reviewer=reviewer,
            rating=rating
        )

    @staticmethod
    def has_user_reviewed(company: Company, reviewer: User):
        """returns True if user has reviewed company else False"""
        return Review.objects.filter(company=company, reviewer=reviewer).exists()
