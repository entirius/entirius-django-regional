# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django_regional.models.currency import Currency
from django_regional.schemas.responses.currency import CurrencyResponse


def list_all() -> list[CurrencyResponse]:
    return [
        CurrencyResponse(id=row.id, iso3=row.iso3, name_en=row.name_en, name_pl=row.name_pl, symbol=row.symbol)
        for row in Currency.objects.all().order_by("iso3")
    ]
