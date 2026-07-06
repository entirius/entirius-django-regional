# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django_regional.models.country import Country
from django_regional.schemas.responses.country import CountryResponse


def list_all() -> list[CountryResponse]:
    return [
        CountryResponse(
            id=row.id,
            iso2=row.iso2,
            iso3=row.iso3,
            name_en=row.name_en,
            name_pl=row.name_pl,
            prefix=row.prefix,
            default_currency_id=row.default_currency_id,
        )
        for row in Country.objects.all().order_by("name_en")
    ]
