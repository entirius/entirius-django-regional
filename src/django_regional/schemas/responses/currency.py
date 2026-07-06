# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from pydantic import BaseModel, Field


class CurrencyResponse(BaseModel):
    id: int = Field(description="Database PK; stable per install, NOT portable across installs", examples=[3])
    iso3: str = Field(description="ISO 4217 three-letter code, uppercase", examples=["EUR"])
    name_en: str = Field(description="English name", examples=["Euro"])
    name_pl: str = Field(description="Polish name", examples=["Euro"])
    symbol: str = Field(description="Currency symbol", examples=["€"])


class CurrencyListResponse(BaseModel):
    count: int = Field(description="Total items in this response", examples=[6])
    next: str | None = Field(None, description="Always null (unpaginated)")
    previous: str | None = Field(None, description="Always null (unpaginated)")
    results: list[CurrencyResponse]
