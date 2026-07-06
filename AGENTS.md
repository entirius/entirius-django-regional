# AGENTS.md

Regional reference data for Volkanos services — distribution `entirius-django-regional`, Django app `django_regional`.
Owns the `Country`, `Language`, and `Currency` tables used across all Volkanos modules. Ships a YAML fixture
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
- Default: do not commit — git is the user's call.

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

## Migrations

`0001_squashed_0006_country_default_currency` is a squash of the historical chain: full final schema plus the
seed data (countries with dialling prefixes, currency symbols, default currencies). Databases that already ran
the original 0001–0006 chain are recognised via `replaces` and record the squash without executing anything;
fresh installs run the single migration. Never edit it — additive changes go into new migrations.

## Data Model

| Entity | Key Fields | Relationships |
|---|---|---|
| Country | iso2 (case-insensitive unique), iso3 (case-insensitive unique), name_en, name_pl, prefix (phone dialling code), default_currency | FK -> Currency (SET_NULL) |
| Language | iso2 (unique), iso3 (unique), name_en, name_pl, name_source | (stand-alone) |
| Currency | iso3 (unique), name_en, name_pl, symbol | (stand-alone) |

Case-insensitive constraints on Country use `UniqueConstraint(Lower("iso2"), ...)` — data loaded with mixed case
will still collide.

Lookup helpers:
- `Country.getFromIso2(str)` — expects upper-case `iso2`, matches against upper-cased value
- `Language.getFromIso2(str)` — lower-cases the input (per Volkanos convention: `Language.iso2` is lowercase)
- `Currency.getFromiso3(str)` — upper-cases input

Rule: always lookup by ISO code (`iso2` for Country / Language, `iso3` for Currency), never by PK — PKs are stable
per fixture run but not portable across installs.

## Fixtures

Single source of truth: `src/django_regional/fixtures/regional-defaults.yaml`. Loaded via
`python manage.py loaddata regional-defaults`. Typical entrypoint ordering puts this fixture first, before any
module that references these tables.

## Anti-Mutation

`Country.save()` raises `Exception("You can not overwrite Country data")`. Adding or amending countries is done via:

1. Migration — extend / amend the fixture, write a `RunPython` migration
2. `loaddata regional-defaults` — re-runs the YAML against the DB

Language and Currency can be saved normally — but the idiom is the same: amend the fixture and `loaddata`.

## Public API

Admin v2 API (read-only, `IsAdminUser` = staff or superuser, JWT auth, unpaginated):

| Method | Path | Returns |
|---|---|---|
| GET | `/api/regional/v2/admin/languages/` | `{"results": [{id, iso2, iso3, name_en, name_pl}, ...]}` ordered by `name_pl` |
| GET | `/api/regional/v2/admin/currencies/` | `{"results": [{id, iso3, name_en, name_pl, symbol}, ...]}` ordered by `iso3` |
| GET | `/api/regional/v2/admin/countries/` | `{"results": [{id, iso2, iso3, name_en, name_pl, prefix, default_currency_id}, ...]}` ordered by `name_en` |

Mounted by consumer via `path("", include("django_regional.urls"))`. The OpenAPI schema is auto-generated by
drf-spectacular when the consumer service mounts `/api/schema/`.

The legacy `serializers.py` (CountrySerializer, LanguageSerializer) is kept for backwards compatibility but new
consumers should use the v2 API.

## Gotchas

- `Country.save` raises — never try to create Countries programmatically, always via fixtures / migrations.
- Country `iso2` is stored **upper-case** (e.g., `"PL"`); Language `iso2` is **lower-case** (e.g., `"pl"`).
  This is the global Volkanos convention and every module assumes it.
- EU uses two region codes where ISO2 and driving-country diverge: `iso2="EL"` maps to Greece (matches EU VAT
  convention), `iso2="GB"` and separate `iso2` for Northern Ireland — check the fixture before coding lookups.
- `Country.prefix` is the phone dialling code with `"+"` prefix (e.g., `"+48"` for Poland). Already includes the `+`.
- `Language.name_source` defaults to empty string — populate it if your module displays language names in the
  user's own language.
- `default_currency` on Country is nullable — old rows may have `NULL`. Consumers must handle that.
