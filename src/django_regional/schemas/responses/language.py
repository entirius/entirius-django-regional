# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from pydantic import BaseModel, Field


class LanguageResponse(BaseModel):
    id: int = Field(description="Database PK; stable per install, NOT portable across installs", examples=[1])
    iso2: str = Field(description="ISO 639-1 two-letter code, lowercase", examples=["en"])
    iso3: str = Field(description="ISO 639-2 three-letter code, lowercase", examples=["eng"])
    name_en: str = Field(description="English name", examples=["English"])
    name_pl: str = Field(description="Polish name", examples=["angielski"])


class LanguageListResponse(BaseModel):
    count: int = Field(description="Total items in this response", examples=[12])
    next: str | None = Field(None, description="Always null (unpaginated)")
    previous: str | None = Field(None, description="Always null (unpaginated)")
    results: list[LanguageResponse]
