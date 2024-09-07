from django.core.management.base import BaseCommand
from django.utils.text import slugify
from core.models import Industry, Country, City, Currency
import re


class Command(BaseCommand):
    help = "Populate database with industries, countries, cities, currencies"

    def add_arguments(self, parser):
        parser.add_argument("--industry", type=str, help="Path to industries file")
        parser.add_argument("--country", type=str, help="Path to countries file")
        parser.add_argument("--city", type=str, help="Path to cities file")
        parser.add_argument("--currency", type=str, help="Path to currencies file")

    def handle(self, *args, **options):

        if options["industry"]:
            self.populate_industries(options["industry"])
        if options["country"]:
            self.populate_countries(options["country"])
        if options["city"]:
            self.populate_cities(options["city"])
        if options["currency"]:
            self.populate_currencies(options["currency"])

    def populate_industries(self, file_path):
        with open(file_path, "r") as file:
            industries = file.read().split("\n")
            for industry in industries:
                Industry.objects.get_or_create(name=industry)

        self.stdout.write(
            self.style.SUCCESS("Successfully added industries to database")
        )

    def populate_countries(self, file_path):
        pass

    def populate_cities(self, file_path):
        pass

    def populate_currencies(self, file_path):
        with open(file_path, "r") as f:
            for line in f.readlines():
                currency = line.strip()
                c_code = re.search(r"\(([A-Z]{3})\)", currency).group(1)
                c_name = currency[: currency.find("(") - 1]
                Currency.objects.get_or_create(name=c_name, code=c_code)
        self.stdout.write(
            self.style.SUCCESS("Successfully added currencies to database")
        )
