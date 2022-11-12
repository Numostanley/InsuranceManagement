from django.test import TestCase
from apps.users.models import User
from factory.django import DjangoModelFactory

class UserFactory(DjangoModelFactory):
    email = "gabby@example.com"
    username = "gabby_fred"
    first_name = "gabriel"
    last_name = "fred"
    phone_number = "23476859385"
    location = "Nigeria"

    class Meta:
        model = User