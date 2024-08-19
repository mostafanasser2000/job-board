from django.test import TestCase
from core.models import Job, Industry, Company, Skill
from django.core.exceptions import ValidationError
from django.utils.text import slugify


class IndustryModelTest(TestCase):
    def test_industry_creation(self):
        industry = Industry.objects.create(name="Technology")
        self.assertEqual(industry.name, "Technology")
        self.assertEqual(industry.slug, slugify("Technology"))
        self.assertEqual(str(industry), "Technology")


# class LocationModelTest(TestCase):
#     def test_location_creation(self):
#         location = Location.objects.create(city="Cairo", country="Egypt")
#         self.assertEqual(location.city, "Cairo")
#         self.assertEqual(location.country, "Egypt")
#         self.assertEqual(str(location), "Cairo, Egypt")


class CompanyModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.COMPANY_SIZE_CHOICES = [
            (1, "1-10"),
            (2, "11-50"),
            (3, "51-200"),
            (4, "201-500"),
            (5, "501-1000"),
            (6, "1001+"),
        ]
        cls.industry = Industry.objects.create(name="Technology")
        # cls.location = Location.objects.create(city="Cairo", country="Egypt")

    def test_company_creation(self):
        company = Company.objects.create(name="Test Company", company_size=1)

        company.industries.add(self.industry)
        self.assertEqual(company.name, "Test Company")
        self.assertEqual(company.slug, slugify("Test Company"))
        # self.assertEqual(company.location, self.location)
        self.assertEqual(company.total_employees(), self.COMPANY_SIZE_CHOICES[1][1])
        self.assertEqual(company.industries.first(), self.industry)
        self.assertEqual(str(company), "Test Company")


class SkillModelTest(TestCase):
    def test_skill_creation(self):
        skill = Skill.objects.create(name="Django")
        self.assertEqual(skill.name, "Django")
        self.assertEqual(skill.slug, slugify("Django"))
        self.assertEqual(str(skill), "Django")


class JobModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # cls.location = Location.objects.create(city="Cairo", country="Egypt")
        cls.company = Company.objects.create(name="Test Company")

        cls.skill = Skill.objects.create(name="Django")

    def test_job_creation(self):
        job = Job.objects.create(
            title="Django Developer",
            company=self.company,
            # location=self.location,
            workplace_type="Remote",
            work_type="Full Time",
        )
        job.skills_required.add(self.skill)

        self.assertEqual(job.title, "Django Developer")
        self.assertEqual(job.slug, slugify(f"{job.title}-{job.company.name}-{job.id}"))
        # self.assertEqual(job.location, self.location)
        self.assertEqual(job.company, self.company)
        self.assertEqual(job.workplace_type, "Remote")
        self.assertEqual(job.work_type, "Full Time")
        self.assertEqual(job.skills_required.first(), self.skill)
        self.assertEqual(str(job), f"{job.title} at {job.company.name}")

    def test_salary_validation(self):
        with self.assertRaises(ValidationError):
            job = Job.objects.create(
                title="Job with invalid range",
                company=self.company,
                # location=self.location,
                salary_lowest=20000,
                salary_highest=15000,
            )
            job.full_clean()

    def test_salary_range(self):
        job = Job.objects.create(
            title="Job with valid range",
            company=self.company,
            # location=self.location,
            salary_lowest=1500,
            salary_highest=2000,
        )
        self.assertEqual(job.salary_range, "1500 - 2000 USD")

        job = Job.objects.create(
            title="Job with min",
            company=self.company,
            # location=self.location,
            salary_lowest=1500,
        )
        self.assertEqual(job.salary_range, "From 1500 USD")

        job = Job.objects.create(
            title="Job with max",
            company=self.company,
            # location=self.location,
            salary_highest=2000,
        )
        self.assertEqual(job.salary_range, "Up to 2000 USD")
