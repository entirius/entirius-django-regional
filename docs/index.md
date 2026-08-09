---
title: Regional
description: Single source of truth for ISO reference data — countries, languages, currencies — used across the Volkanos stack.
sidebar:
  label: Overview
  collapsed: true
---

django-regional owns the `Country`, `Language`, and `Currency` reference tables that every other module FK's into. Data is fixture-driven and immutable by convention — edits go through `regional-defaults.yaml` and migrations, never through admin CRUD.

## What It Does

- Stores ISO 3166-1 countries (`iso2`, `iso3`, `name_en`, `name_pl`, `prefix`, optional `default_currency`)
- Stores ISO 639-1 languages (`iso2` lowercase, `iso3`, `name_en`, `name_pl`, `name_source`)
- Stores ISO 4217 currencies (`iso3` uppercase, `name_en`, `name_pl`, `symbol`)
- Ships a 490-line `regional-defaults.yaml` fixture seeding ~250 countries + canonical languages + 6 currencies
- Exposes a read-only admin API (since 1.7.0) for CMS panels and integrators that need lookup tables

## Architecture

```
django_regional/
├── models/                         # Country, Language, Currency
├── fixtures/regional-defaults.yaml # Single source of truth — load on bootstrap
├── api/admin/                      # Read-only list endpoints (1.7.0+)
│   ├── permissions.py              # IsAdminUser (staff or superuser)
│   ├── urls.py                     # 3 paths
│   └── views/                      # language, currency, country APIView
├── services/                       # Thin list_all() per resource → list[Pydantic]
├── schemas/responses/              # Pydantic response models (id, iso codes, names, symbol)
└── urls.py                         # Mount /api/regional/v2/admin/
```

## Data Model

| Entity | Key Fields | Notes |
|---|---|---|
| Country | `iso2` (uppercase, case-insensitive unique), `iso3`, `name_en`, `name_pl`, `prefix`, `default_currency` (FK→Currency, SET_NULL) | `Country.save()` raises — fixture-only |
| Language | `iso2` (lowercase unique), `iso3`, `name_en`, `name_pl`, `name_source` | Lowercase per Volkanos convention |
| Currency | `iso3` (uppercase unique), `name_en`, `name_pl`, `symbol` | Standard ISO 4217 |

**Case convention:** Country `iso2` is uppercase (`"PL"`), Language `iso2` is lowercase (`"pl"`). Every module assumes this.

## Admin API (1.7.0+)

URL prefix: `/api/regional/v2/admin/`. Auth: `JWTAuthentication` + `IsAdminUser` (staff or superuser). Read-only, unpaginated (datasets are small and bounded).

| Method | Path | Returns |
|---|---|---|
| GET | `/languages/` | `{count, next:null, previous:null, results: [{id, iso2, iso3, name_en, name_pl}, ...]}` ordered by `name_pl` |
| GET | `/currencies/` | `{count, next:null, previous:null, results: [{id, iso3, name_en, name_pl, symbol}, ...]}` ordered by `iso3` |
| GET | `/countries/` | `{count, next:null, previous:null, results: [{id, iso2, iso3, name_en, name_pl, prefix, default_currency_id}, ...]}` ordered by `name_en` |

Response envelope follows the standard pagination shape from `api-response-contract` (`count`, `next`, `previous`, `results`) even though endpoints are unpaginated — keeps consumers compatible with the platform-wide envelope contract.

## Consumers

| Module | How it uses regional |
|---|---|
| `django-pim` | `Channel.languages` M2M, `Channel.default_language` / `default_currency` FK |
| `django-pricemanager` | `CurrentPrice.country` / `currency` FK (3.1.0+), `PriceHistory.currency`, `PriceList.currency` |
| `django-checkout` | `ShippingOption.currency`, `PaymentMethod.currencies`, `DiscountRuleCode.currencies` |
| `django-suppliers` | `Supplier.default_language` / `default_currency` / `country` FK |
| `django-deliverypoints` | Proxies regional countries via own `/api/deliverypoints/v2/admin/countries/` (legacy — will deprecate, callers should migrate to `/regional/v2/admin/countries/`) |
| `django-omnibus` | `Currency` consumer via FK (since 2.0.0) |
| `cms-blueprint` | `useRegionalStore` Pinia store fetches all three lists once per session, exposes `languageOptions` / `currencyOptions` / `countryOptions` for dropdowns |

## Fixture & Bootstrap

Loaded once during stack setup:

```bash
python manage.py loaddata regional-defaults
```

The fixture is the **single source of truth**. Adding a country, language, or currency means:

1. Append to `src/django_regional/fixtures/regional-defaults.yaml`
2. Write a data migration with `loaddata` or explicit `RunPython`
3. Never via Django admin (Country is hard-locked; Currency/Language are convention-locked)

## Gotchas

- `Country.save()` raises `Exception("You can not overwrite Country data")` — true immutability. Use fixtures + migrations.
- Country `iso2` uppercase, Language `iso2` lowercase. Every consumer assumes this.
- `default_currency` on Country is nullable — handle `None` in consumers.
- Module's API ships standard pagination envelope (`count` always equals `len(results)`, `next`/`previous` always `null`). Don't try to follow `next` — there isn't one.
- Some countries in the fixture diverge from strict ISO (e.g. `iso2="EL"` for Greece matching EU VAT convention).
- Two-step migration consumers (PM 0021): if a downstream module migrates FKs into regional and finds an unseeded ISO code, it should **fail loud** — never lazy-create regional rows from migration data (regional stays fixture-driven).
