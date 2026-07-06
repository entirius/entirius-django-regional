# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.db import models
from django.db.models.functions import Lower


class Country(models.Model):
    iso2 = models.CharField(max_length=2)
    iso3 = models.CharField(max_length=3)
    name_en = models.CharField(max_length=100, null=False, blank=False)
    name_pl = models.CharField(max_length=100, null=False, blank=False)
    prefix = models.CharField(max_length=32, null=False, blank=False, default="")
    default_currency = models.ForeignKey("Currency", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return "%s %s %s %s" % (self.iso2, self.iso3, self.name_pl, self.prefix)

    def getFromIso2(country_str):
        return Country.objects.get(iso2=country_str.upper())

    @property
    def code(self):
        return self.iso2

    def save(self, *args, **kwargs):
        raise Exception("You can not overwrite Country data")

    class Meta:
        ordering = ["iso3"]
        verbose_name_plural = "countries"
        constraints = [
            models.UniqueConstraint(Lower("iso2"), name="country_unique_iso2"),
            models.UniqueConstraint(Lower("iso3"), name="country_unique_iso3"),
        ]
