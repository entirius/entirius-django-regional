# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from pydantic import BaseModel, Field


class CountryResponse(BaseModel):
    id: int = Field(description="Database PK; stable per install, NOT portable across installs", examples=[1])
    iso2: str = Field(description="ISO 3166-1 alpha-2 code, uppercase", examples=["PL"])
    iso3: str = Field(description="ISO 3166-1 alpha-3 code, uppercase", examples=["POL"])
    name_en: str = Field(description="English name", examples=["Poland"])
    name_pl: str = Field(description="Polish name", examples=["Polska"])
    prefix: str = Field(description="Phone dialling code", examples=["+48"])
    default_currency_id: int | None = Field(None, description="Default currency PK; null if not set", examples=[3])


class CountryListResponse(BaseModel):
    count: int = Field(description="Total items in this response", examples=[250])
    next: str | None = Field(None, description="Always null (unpaginated)")
    previous: str | None = Field(None, description="Always null (unpaginated)")
    results: list[CountryResponse]
