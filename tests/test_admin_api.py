# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""Admin API tests — auth gates + happy path for languages/currencies/countries."""

import pytest
from rest_framework import status

_LANGUAGES_URL = "/api/regional/v2/admin/languages/"
_CURRENCIES_URL = "/api/regional/v2/admin/currencies/"
_COUNTRIES_URL = "/api/regional/v2/admin/countries/"


# Auth gates -----------------------------------------------------------------


@pytest.mark.django_db
@pytest.mark.parametrize("url", [_LANGUAGES_URL, _CURRENCIES_URL, _COUNTRIES_URL])
def test_unauthenticated_request_returns_401(api_client, url):
    response = api_client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
@pytest.mark.parametrize("url", [_LANGUAGES_URL, _CURRENCIES_URL, _COUNTRIES_URL])
def test_regular_user_forbidden(regular_client, url):
    response = regular_client.get(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN


# Languages ------------------------------------------------------------------


@pytest.mark.django_db
def test_list_languages_returns_seeded_rows(admin_client, seed_languages):
    response = admin_client.get(_LANGUAGES_URL)
    assert response.status_code == status.HTTP_200_OK
    body = response.json()
    assert "results" in body
    iso2s = {row["iso2"] for row in body["results"]}
    assert {"en", "pl", "de"}.issubset(iso2s)
    row = next(r for r in body["results"] if r["iso2"] == "en")
    assert row["iso3"] == "eng"
    assert row["name_en"] == "English"
    assert row["name_pl"] == "angielski"
    assert isinstance(row["id"], int)


@pytest.mark.django_db
def test_list_languages_orders_by_name_pl(admin_client, seed_languages):
    response = admin_client.get(_LANGUAGES_URL)
    name_pls = [row["name_pl"] for row in response.json()["results"]]
    assert name_pls == sorted(name_pls)


# Currencies -----------------------------------------------------------------


@pytest.mark.django_db
def test_list_currencies_returns_seeded_rows(admin_client, seed_currencies):
    response = admin_client.get(_CURRENCIES_URL)
    assert response.status_code == status.HTTP_200_OK
    iso3s = {row["iso3"] for row in response.json()["results"]}
    assert {"PLN", "EUR", "USD"}.issubset(iso3s)
    eur = next(r for r in response.json()["results"] if r["iso3"] == "EUR")
    assert eur["name_en"] == "Euro"
    assert eur["symbol"] == "€"


@pytest.mark.django_db
def test_list_currencies_orders_by_iso3(admin_client, seed_currencies):
    response = admin_client.get(_CURRENCIES_URL)
    iso3s = [row["iso3"] for row in response.json()["results"]]
    assert iso3s == sorted(iso3s)


# Countries ------------------------------------------------------------------


@pytest.mark.django_db
def test_list_countries_returns_seeded_rows(admin_client, seed_countries):
    response = admin_client.get(_COUNTRIES_URL)
    assert response.status_code == status.HTTP_200_OK
    iso2s = {row["iso2"] for row in response.json()["results"]}
    assert {"PL", "DE"}.issubset(iso2s)
    pl = next(r for r in response.json()["results"] if r["iso2"] == "PL")
    assert pl["iso3"] == "POL"
    assert pl["prefix"] == "+48"
    assert pl["default_currency_id"] is not None


@pytest.mark.django_db
def test_list_countries_default_currency_id_nullable(admin_client, db):
    from django_regional.models.country import Country

    Country.objects.bulk_create([Country(iso2="XX", iso3="XXX", name_en="Xland", name_pl="Xkrain", prefix="+0")])
    response = admin_client.get(_COUNTRIES_URL)
    xland = next(r for r in response.json()["results"] if r["iso2"] == "XX")
    assert xland["default_currency_id"] is None


# Schema sanity --------------------------------------------------------------


@pytest.mark.django_db
def test_response_envelope_matches_standard_pagination_shape(admin_client, seed_languages):
    """Response envelope is {count, next, previous, results} per api-response-contract standard pagination.
    Endpoint is unpaginated so next/previous are always None and count = len(results)."""
    body = admin_client.get(_LANGUAGES_URL).json()
    assert set(body.keys()) == {"count", "next", "previous", "results"}
    assert isinstance(body["results"], list)
    assert body["count"] == len(body["results"])
    assert body["next"] is None
    assert body["previous"] is None
