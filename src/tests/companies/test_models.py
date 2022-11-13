from django.test import TestCase
from apps.companies.models import Company
from factory.django import DjangoModelFactory
from tests.users.test_models import UserFactory

class CompanyFactory(DjangoModelFactory):
    name = "CyberMe"
    email = "cyberme@example.com"
    website = "www.cyberme.com"
    location = "Nigeria"

    class Meta:
        model = Company

class CompanyModelTest(TestCase):

    def setUp(self):
        self.company = CompanyFactory.create(
            user=UserFactory.create(
                username="allen",
                email="allen@gmail.com"
                )
            )

    def test_string_representation(self):
        self.assertEqual(str(self.company), self.company.name)

    def test_get_all_active_companies(self):
        self.company2 = CompanyFactory.create(
            user = UserFactory.create(
                username="barry",
                email="barry@gmail.com"
                ),
            name = "faxti",
            email = "barry@gmail.com",
            contact = "23486443638844",
            website = "www.skirle.com"
            )
        all_active_companies = Company.get_all_active_companies()
        self.assert_(len(all_active_companies) == 2)

    def test_get_company_by_id(self):
        company = Company.get_company_by_id("1")
        company2 = Company.get_company_by_id("100")
        self.assertEqual(self.company, company)
        self.assertEqual(company2, None)

    def test_get_company_by_name(self):
        company = Company.get_company_by_name("CyberMe")
        company2 = Company.get_company_by_name("Blaze")
        self.assertEqual(self.company, company)
        self.assertEqual(company2, None)

    def test_delete_company_by_id(self):
        company = Company.delete_company_by_id("1")
        self.assertEqual(self.company, company)


