from django.db import models
from django.utils import timezone

from apps import helpers
from apps.users.models import User


class Company(models.Model):
    user = models.OneToOneField(User, related_name='company', on_delete=models.CASCADE)
    name = models.CharField(max_length=200, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    contact = models.CharField(max_length=50, unique=True)
    photo = models.ImageField(default='', upload_to=helpers.save_company_image)

    is_deleted = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now_add=timezone.now)

    website = models.URLField(unique=True)
    location = models.TextField()

    def __str__(self):
        return self.name

    @staticmethod
    def get_all_active_companies():
        """return list of all companies that are not deleted"""
        return Company.objects.filter(is_deleted=False)

    @staticmethod
    def get_company_by_id(id: str):
        """retrieve company by id"""
        try:
            return Company.objects.get(id=id)
        except Company.DoesNotExist:
            return None

    @staticmethod
    def get_company_by_name(name: str):
        """retrieve company by name"""
        try:
            return Company.objects.get(name=name)
        except Company.DoesNotExist:
            return None

    @staticmethod
    def get_company_by_email(email: str):
        """retrieve company by email"""
        try:
            return Company.objects.get(email=email)
        except Company.DoesNotExist:
            return None

    @staticmethod
    def get_company_by_website(website: str):
        """retrieve company by website"""
        try:
            return Company.objects.get(website=website)
        except Company.DoesNotExist:
            return None

    @staticmethod
    def get_company_by_contact(contact: str):
        """retrieve company by contact"""
        try:
            return Company.objects.get(contaxt=contact)
        except Company.DoesNotExist:
            return None

    @staticmethod
    def delete_company_by_id(id: str):
        """retrieve company by name"""
        try:
            company = Company.get_company_by_id(id)
            company.is_deleted = True
            return company
        except Company.DoesNotExist:
            return None
