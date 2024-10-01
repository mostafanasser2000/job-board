from django.core.exceptions import ValidationError
from django.test import TestCase
from posts.models import JobPost
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from core.models import Currency, Skill, Country

User = get_user_model()


class JobPostModelTest(TestCase):
    def setUp(self):
        self.publisher = User.objects.create_user(email='testcompany@gmail.com',
                                                  password='testpass123', is_company=True)
        self.currency, created = Currency.objects.get_or_create(code='USD')
        self.country, created = Country.objects.get_or_create(name='Egypt')

    def test_create_post(self):
        post = JobPost.objects.create(
            title='Software Engineer',
            publisher=self.publisher,
            description='Looking for a experienced software engineer',
            country=self.country,
            workplace_type='on-site',
            work_type='full-time',
            start_salary=1000,
            end_salary=2000,
            currency=self.currency
        )
        self.assertEqual(post.title, 'Software Engineer')
        self.assertEqual(post.publisher, self.publisher)
        self.assertEqual(post.country, self.country)
        self.assertEqual(post.slug, slugify(f'{post.title}-at-{post.publisher}-{post.pk}'))
        self.assertEqual(post.get_absolute_url(), f'/jobs/{post.slug}/')
        self.assertEqual(str(post), f'{post.title} at {post.publisher}')

    def test_salary_validation(self):
        post = JobPost.objects.create(
            title='Software Engineer',
            publisher=self.publisher,
            country=self.country,
            description='Looking for a experienced software engineer',
            workplace_type='on-site',
            work_type='full-time',
            start_salary=2000,
            end_salary=1000,
            currency=self.currency
        )
        with self.assertRaises(ValidationError):
            post.clean()

    # def test_only_companies_can_publish(self):
    #     normal_user = User.objects.create_user(email='user@gmail.com', password='testpass123', is_company=False)
    #     post = JobPost.objects.create(
    #         title='Software Engineer',
    #         publisher=normal_user,
    #         country=self.country,
    #         description='Looking for a experienced software engineer',
    #         workplace_type='on-site',
    #         work_type='full-time',
    #         start_salary=2000,
    #         end_salary=1000,
    #         currency=self.currency
    #     )
    #     with self.assertRaises(ValidationError):
    #         post.clean()
