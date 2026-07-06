# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.contrib import admin

from .models import Country, Currency, Language


class CountryAdmin(admin.ModelAdmin):
    list_display = ("iso2", "iso3", "name_en", "prefix", "default_currency")
    list_filter = ("default_currency",)
    search_fields = ("iso2", "iso3", "name_en", "name_pl", "prefix")


class LanguageAdmin(admin.ModelAdmin):
    list_display = ("iso2", "iso3", "name_en", "name_pl", "name_source")
    search_fields = ("iso2", "iso3", "name_en", "name_pl", "name_source")


class CurrencyAdmin(admin.ModelAdmin):
    list_display = ("iso3", "name_en", "name_pl")
    search_fields = ("iso3", "name_en", "name_pl")


admin.site.register(Country, CountryAdmin)
admin.site.register(Currency, CurrencyAdmin)
admin.site.register(Language, LanguageAdmin)
