from django.core.management.base import BaseCommand
from django.utils.text import slugify
from core.models import Industry, Location, Skill


class Command(BaseCommand):
    help = "Populate database with industries, locations and skills"

    def add_arguments(self, parser):
        parser.add_argument("--locations", type=str, help="Path to locations file")
        parser.add_argument("--skills", type=str, help="Path to skills file")

    def handle(self, *args, **options):
        if options["locations"]:
            self.populate_locations(options["locations"])

        if options["skills"]:
            self.populate_skills(options["skills"])

        if options["industries"]:
            self.populate_industries(options["industries"])

    def populate_locations(self, file_path):
        pass

    def populate_skills(self, file_path):
        with open(file_path, "r") as file:
            skills = file.read().split("\n")
            for skill in skills:
                Skill.objects.get_or_create(name=skill)

        self.stdout.write(self.style.SUCCESS("Successfully added skills to database"))

    def populate_industries(self, file_path):
        with open(file_path, "r") as file:
            industries = file.read().split("\n")
            for industry in industries:
                Industry.objects.get_or_create(name=industry)

        self.stdout.write(
            self.style.SUCCESS("Successfully added industries to database")
        )
