# AGENTS.md

`entirius-django-regional` (Django app `django_regional`) — regional reference data for Entirius services.
Owns the `Country`, `Language`, and `Currency` tables used across all Entirius modules. Ships a YAML fixture
(`regional-defaults.yaml`) with EU countries, common languages, and currencies. Country rows are immutable by design
(`Country.save` raises) — updates go through fixtures and migrations.

## Commands

| Command | Meaning |
|---|---|
| `make install` | sync dependencies (uv, incl. extras) |
| `make check` | lint + format-check (ruff) |
| `make fix` | auto-fix lint + format |
| `make test` | test suite (pytest + pytest-django, sqlite in-memory) |

## Conventions

- English only: code, docs, commits, branches, PRs.
- MPL-2.0: every non-trivial source file carries the license header (pre-commit inserts it).
- Toolchain: uv + ruff + hatchling + pytest; all config in `pyproject.toml`; `uv.lock` committed.
- Git flow: `master` (production) + `develop` (integration); changes land via PR; semver tag on `master`.
- Never rename the package / Django app_label / DB table prefix `django_regional` — it is a schema contract.
- Migrations are part of the public contract — never edit an already released migration.
- Access: areas live on the AppConfig (`access_areas`, `access_route_rules`), every admin view carries
  `access_area`; a new admin route without one fails `tests/test_access_ownership.py`.
- Default: do not commit — git is the user's call.
- No AI attribution in commits or PR descriptions.

## Architecture

```
src/django_regional/
├── models/
│   ├── country.py       # Country (iso2, iso3, name_en, name_pl, prefix, default_currency)
│   ├── language.py      # Language (iso2 unique, iso3 unique, name_en, name_pl, name_source)
│   └── currency.py      # Currency (iso3 unique, name_en, name_pl, symbol)
│
├── api/
│   └── admin/
│       ├── permissions.py        # IsAdminUser (staff or superuser)
│       ├── urls.py               # mounts language/currency/country list views
│       └── views/                # APIView per resource — read-only list
│
├── services/            # list_all() -> list[<Resource>Response] per resource
├── schemas/responses/   # Pydantic response models
├── managers/
├── fixtures/
│   └── regional-defaults.yaml   # Seeds countries + languages + currencies
│
├── serializers.py       # CountrySerializer, LanguageSerializer (DRF, legacy)
├── admin.py             # CountryAdmin / LanguageAdmin / CurrencyAdmin
├── urls.py              # Root URL config, mounts api/admin/urls under /api/regional/v2/admin/
├── apps.py
└── migrations/          # single squashed initial (replaces the historical 0001-0006 chain)
```

Reference data is read-only: `Country.save()` raises; countries, languages and currencies change through the
`regional-defaults` fixture and migrations, never through admin CRUD. Always look rows up by ISO code, never by PK.

| Topic | Where |
|---|---|
| Overview, consumers, admin API | `docs/index.md` |
| Entities, lookup helpers, migrations, admin API responses | `docs/data-model.md` |
| Fixture and how to change reference data | `docs/fixtures.md` |

## Gotchas

- `Country.save` raises — never try to create Countries programmatically, always via fixtures / migrations.
- Country `iso2` is stored **upper-case** (e.g., `"PL"`); Language `iso2` is **lower-case** (e.g., `"pl"`).
  This is the platform-wide convention and every module assumes it.
- EU uses two region codes where ISO2 and driving-country diverge: `iso2="EL"` maps to Greece (matches EU VAT
  convention), `iso2="GB"` and separate `iso2` for Northern Ireland — check the fixture before coding lookups.
- `Country.prefix` is the phone dialling code with `"+"` prefix (e.g., `"+48"` for Poland). Already includes the `+`.
- `Language.name_source` defaults to empty string — populate it if your module displays language names in the
  user's own language.
- `default_currency` on Country is nullable — old rows may have `NULL`. Consumers must handle that.
