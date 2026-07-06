# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django_regional.models.language import Language
from django_regional.schemas.responses.language import LanguageResponse


def list_all() -> list[LanguageResponse]:
    return [
        LanguageResponse(id=row.id, iso2=row.iso2, iso3=row.iso3, name_en=row.name_en, name_pl=row.name_pl)
        for row in Language.objects.all().order_by("name_pl")
    ]
