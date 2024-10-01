from django.test import TestCase
from .models import Country, Currency, Skill, Industry


class CountryModelTests(TestCase):
    def test_create_country(self):
        country = Country.objects.create(name="Egypt")
        self.assertEqual(country.name, "Egypt")
        self.assertEqual(country.slug, "egypt")
        self.assertEqual(str(country), "Egypt")


class CurrencyModelTests(TestCase):
    def test_create_currency(self):
        currency = Currency.objects.create(name="Egyptian Pound", code="EGP")
        self.assertEqual(currency.name, "Egyptian Pound")
        self.assertEqual(currency.code, "EGP")
        self.assertEqual(str(currency), "Egyptian Pound (EGP)")


class SkillModelTests(TestCase):
    def test_create_skill(self):
        skill = Skill.objects.create(name="Python")
        self.assertEqual(skill.name, "Python")
        self.assertEqual(str(skill), "Python")


class IndustryModelTests(TestCase):
    def test_create_industry(self):
        industry = Industry.objects.create(name="Technology")
        self.assertEqual(industry.name, "Technology")
        self.assertEqual(str(industry), "Technology")
