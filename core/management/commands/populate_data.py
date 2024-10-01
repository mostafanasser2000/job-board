import re
from core.models import Industry, Country, Currency, Skill
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Populate database with industries, countries, skills, currencies"

    def add_arguments(self, parser):
        parser.add_argument("--industry", type=str, help="Path to industries file")
        parser.add_argument("--country", type=str, help="Path to countries file")
        parser.add_argument("--skills", type=str, help="Path to skills file")
        parser.add_argument("--currency", type=str, help="Path to currencies file")

    def handle(self, *args, **options):

        if options["industry"]:
            self.populate_industries(options["industry"])
        if options["country"]:
            self.populate_countries(options["country"])
        if options["skills"]:
            self.populate_skills(options["skills"])
        if options["currency"]:
            self.populate_currencies(options["currency"])

    def populate_industries(self, file_path):
        with open(file_path, "r") as f:
            for line in f.readlines():
                industry = line.strip()
                if industry:
                    Industry.objects.get_or_create(name=industry)

        self.stdout.write(
            self.style.SUCCESS("Successfully added industries to database")
        )

    def populate_countries(self, file_path):
        with open(file_path, "r") as f:
            for line in f.readlines():
                country = line.strip()
                if country:
                    Country.objects.get_or_create(name=country)
        self.stdout.write(self.style.SUCCESS("Successfully added countries to database"))

    def populate_skills(self, file_path):
        with open(file_path, "r") as f:
            for line in f.readlines():
                skill = line.strip()
                if skill:
                    Skill.objects.get_or_create(name=skill)
        self.stdout.write(self.style.SUCCESS("Successfully added skills to database"))

    def populate_currencies(self, file_path):
        with open(file_path, "r") as f:
            for line in f.readlines():
                currency = line.strip()
                if currency:
                    c_code = re.search(r"\(([A-Z]{3})\)", currency).group(1)
                    c_name = currency[: currency.find("(") - 1]
                    Currency.objects.get_or_create(name=c_name, code=c_code)
        self.stdout.write(
            self.style.SUCCESS("Successfully added currencies to database")
        )
