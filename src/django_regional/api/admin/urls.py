# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.urls import path

from django_regional.api.admin.views.country_views import CountryListView
from django_regional.api.admin.views.currency_views import CurrencyListView
from django_regional.api.admin.views.language_views import LanguageListView

app_name = "regional-admin"

urlpatterns = [
    path("languages/", LanguageListView.as_view(), name="language-list"),
    path("currencies/", CurrencyListView.as_view(), name="currency-list"),
    path("countries/", CountryListView.as_view(), name="country-list"),
]
