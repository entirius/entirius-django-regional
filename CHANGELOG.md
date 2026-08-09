# Changelog

## 2.0.1 — 2026-07-10

- Reset seeded primary-key sequences on postgres after fixture loads.

## 2.0.0 — 2026-07-06

- Initial public release: canonical reference data for the platform —
  languages, currencies, and countries.
- Read-only admin API v2: `/api/regional/v2/admin/{languages,currencies,countries}/`
  (JWT + IsAdminUser, Pydantic responses, standard envelope).
