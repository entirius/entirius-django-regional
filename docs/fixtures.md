---
title: Fixtures
description: The regional-defaults fixture and how reference data is changed.
---

Single source of truth: `src/django_regional/fixtures/regional-defaults.yaml`. Loaded via
`python manage.py loaddata regional-defaults`. Typical entrypoint ordering puts this fixture first, before any
module that references these tables.

## Anti-Mutation

`Country.save()` raises `Exception("You can not overwrite Country data")`. Adding or amending countries is done via:

1. Migration — extend / amend the fixture, write a `RunPython` migration
2. `loaddata regional-defaults` — re-runs the YAML against the DB

Language and Currency can be saved normally — but the idiom is the same: amend the fixture and `loaddata`.
