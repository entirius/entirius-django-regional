# django-regional

Regional reference data for Volkanos services — `Country`, `Currency` and `Language` models with seed data
(countries with dialling prefixes, currency symbols, default currencies), a YAML fixture and a read-only
admin API (`/api/regional/v2/admin/`).

## Installation

```shell
pip install entirius-django-regional
```

Add the app to your project and run migrations:

```python
INSTALLED_APPS = [
    ...
    "django_regional",
]
```

```shell
python manage.py migrate
python manage.py loaddata regional-defaults   # optional: EU defaults fixture
```

Mount the admin API:

```python
urlpatterns = [
    ...
    path("", include("django_regional.urls")),
]
```

## Development

```shell
make install     # sync dependencies (uv)
make check       # lint + format check (ruff)
make test        # test suite (pytest + pytest-django, sqlite in-memory)
```

Development and agent instructions: [AGENTS.md](AGENTS.md).

## License

Mozilla Public License 2.0 — see [LICENSE](LICENSE).
