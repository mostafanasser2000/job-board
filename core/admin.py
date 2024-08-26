from django.contrib import admin
from .models import Country, City, Currency, Industry

# Register your models here.
admin.site.register(Country)
admin.site.register(City)
admin.site.register(Currency)
admin.site.register(Industry)
