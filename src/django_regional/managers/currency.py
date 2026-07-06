# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import logging

from ..models import Currency

logger = logging.getLogger("django")


class CurrencyManager:
    _cache = {}

    def getCurrency(iso3):
        if iso3 is None:
            raise Exception("Currency iso3 was expected, not None")
        iso3 = iso3.upper()
        if iso3 not in CurrencyManager._cache:
            CurrencyManager._cache[iso3] = Currency.objects.get(iso3=iso3)
        return CurrencyManager._cache[iso3]
