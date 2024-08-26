from django.core.management.base import BaseCommand
from django.utils.text import slugify
from core.models import Industry, Country, City, Currency


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
        pass
