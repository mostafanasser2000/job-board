# Generated by Django 5.0.7 on 2024-10-04 19:38

import applications.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0003_alter_application_resume'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='resume',
            field=models.FileField(upload_to=applications.models.upload_resume, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx'], message='Unsupported file extension. Please upload a PDF, DOC, or DOCX file.')]),
        ),
    ]
