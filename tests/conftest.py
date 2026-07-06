# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from django_regional.models.country import Country
from django_regional.models.currency import Currency
from django_regional.models.language import Language


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def admin_user(db) -> User:
    return User.objects.create_superuser(username="admin", email="admin@test.local", password="admin-pass")


@pytest.fixture
def regular_user(db) -> User:
    return User.objects.create_user(username="user", email="user@test.local", password="user-pass")


@pytest.fixture
def admin_client(api_client, admin_user) -> APIClient:
    api_client.force_authenticate(user=admin_user)
    return api_client


@pytest.fixture
def regular_client(api_client, regular_user) -> APIClient:
    api_client.force_authenticate(user=regular_user)
    return api_client


@pytest.fixture
def seed_languages(db) -> list[Language]:
    rows = [
        Language(iso2="en", iso3="eng", name_en="English", name_pl="angielski"),
        Language(iso2="pl", iso3="pol", name_en="Polish", name_pl="polski"),
        Language(iso2="de", iso3="deu", name_en="German", name_pl="niemiecki"),
    ]
    return Language.objects.bulk_create(rows)


@pytest.fixture
def seed_currencies(db) -> list[Currency]:
    rows = [
        Currency(iso3="PLN", name_en="Polish zloty", name_pl="Polski złoty", symbol="zł"),
        Currency(iso3="EUR", name_en="Euro", name_pl="Euro", symbol="€"),
        Currency(iso3="USD", name_en="US Dollar", name_pl="Dolar amerykański", symbol="$"),
    ]
    return Currency.objects.bulk_create(rows)


@pytest.fixture
def seed_countries(db, seed_currencies) -> list[Country]:
    eur = next(c for c in seed_currencies if c.iso3 == "EUR")
    rows = [
        Country(iso2="PL", iso3="POL", name_en="Poland", name_pl="Polska", prefix="+48", default_currency=eur),
        Country(iso2="DE", iso3="DEU", name_en="Germany", name_pl="Niemcy", prefix="+49", default_currency=eur),
    ]
    return Country.objects.bulk_create(rows)
