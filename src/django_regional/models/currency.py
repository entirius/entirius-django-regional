# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.db import models


class Currency(models.Model):
    iso3 = models.CharField(unique=True, max_length=3)
    name_en = models.CharField(max_length=24)
    name_pl = models.CharField(max_length=24)
    symbol = models.CharField(max_length=16, default="")

    def __str__(self):
        return self.iso3

    def getFromiso3(currency_str):
        return Currency.objects.get(iso3=currency_str.upper())

    class Meta:
        ordering = ["iso3"]
        verbose_name_plural = "currencies"
