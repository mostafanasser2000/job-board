from django.contrib import admin
from .models import Job, Industry, Company, Skill

# Register your models here.
admin.site.register(Job)
admin.site.register(Industry)
admin.site.register(Company)
admin.site.register(Skill)
