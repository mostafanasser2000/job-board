from django.contrib import admin

from .models import Currency, Industry, Country, Skill

admin.site.register(Currency)
admin.site.register(Industry)
admin.site.register(Country)
admin.site.register(Skill)
