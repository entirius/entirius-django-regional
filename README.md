# entirius-django-regional

A Django module with regional reference data for Entirius, the open-source modular ecommerce platform: countries, currencies and languages.
Other modules point their foreign keys at these tables; the data ships as a fixture and a read-only admin API lists it.

[![PyPI](https://img.shields.io/pypi/v/entirius-django-regional.svg)](https://pypi.org/project/entirius-django-regional/)
[![Python](https://img.shields.io/pypi/pyversions/entirius-django-regional.svg)](https://pypi.org/project/entirius-django-regional/)
[![License: MPL-2.0](https://img.shields.io/badge/license-MPL--2.0-blue.svg)](https://github.com/entirius/entirius-django-regional/blob/develop/LICENSE)

## What it does

- Provides the `Country`, `Currency` and `Language` models keyed by ISO codes.
- Seeds countries with dialling prefixes, currency symbols and default currencies in its migration.
- Ships the `regional-defaults` fixture as the place where reference data is changed.
- Keeps country rows read-only: `Country.save()` raises, changes go through the fixture and migrations.
- Lists languages, currencies and countries over a read-only admin API under `/api/regional/v2/admin/`.

## Installation

```shell
uv add entirius-django-regional
pip install entirius-django-regional
```

```python
INSTALLED_APPS = [
    ...
    "django_regional",
]

# urls.py
urlpatterns = [
    path("", include("django_regional.urls")),
]
```

```shell
python manage.py migrate
python manage.py loaddata regional-defaults   # optional: the defaults fixture
```

The module has no settings of its own.

## Quick start

```python
from django_regional.models import Country, Currency, Language

country = Country.getFromIso2("PL")       # country codes are stored upper-case
language = Language.getFromIso2("pl")     # language codes are stored lower-case
currency = Currency.getFromiso3("PLN")
```

## Requirements

- Python 3.11 or newer, Django 4.2 or newer.
- Django REST Framework, `djangorestframework-simplejwt`, `pydantic`, `drf-spectacular`, `pyyaml`.
- No other Entirius packages.

## Documentation

- Module docs: https://github.com/entirius/entirius-django-regional/tree/develop/docs
- Entirius documentation: https://docs.entirius.com/
- Changelog: https://github.com/entirius/entirius-django-regional/blob/develop/CHANGELOG.md

## Part of Entirius

This module runs inside the Entirius backend service (Volkanos) as the shared source of countries, currencies and languages.

- Backend service: https://github.com/entirius/entirius-service-volkanos
- Docker harness: https://github.com/entirius/entirius-zeno
- Sibling modules: https://github.com/entirius/entirius-django-pim, https://github.com/entirius/entirius-django-email, https://github.com/entirius/entirius-django-accounts

## Development

```shell
make install     # sync dependencies (uv)
make check       # lint + format check (ruff)
make test        # test suite (pytest + pytest-django, sqlite in-memory)
```

Development and agent instructions: https://github.com/entirius/entirius-django-regional/blob/develop/AGENTS.md

## License

Mozilla Public License 2.0 (MPL-2.0) — see https://github.com/entirius/entirius-django-regional/blob/develop/LICENSE.
