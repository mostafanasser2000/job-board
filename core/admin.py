from django.contrib import admin
from .models import  Currency, Industry
from cities_light.models import Country
# Register your models here.
admin.site.register(Currency)
admin.site.register(Industry)
