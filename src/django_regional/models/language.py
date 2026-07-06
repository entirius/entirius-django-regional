# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.db import models


class Language(models.Model):
    iso2 = models.CharField(unique=True, max_length=2)
    iso3 = models.CharField(unique=True, max_length=3)
    name_en = models.CharField(max_length=16, null=False, blank=False)
    name_pl = models.CharField(max_length=16, null=False, blank=False)
    name_source = models.CharField(max_length=16, null=False, blank=False, default="")

    def __str__(self):
        return "%s %s" % (self.iso2, self.name_pl)

    def getFromIso2(language_str):
        return Language.objects.get(iso2=language_str.lower())

    class Meta:
        ordering = ["name_pl"]
        verbose_name_plural = "languages"
