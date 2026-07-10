# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.db import migrations

# 0001 seeds Country and Currency with explicit primary keys, which leaves the postgres
# identity sequences at their initial value — the next unqualified INSERT collides with
# a seeded id. Advance the sequences to max(id). No-op on sqlite (rowid needs no fix).
SEEDED_TABLES = ("django_regional_country", "django_regional_currency")


def reset_pk_sequences(apps, schema_editor):
    if schema_editor.connection.vendor != "postgresql":
        return
    for table in SEEDED_TABLES:
        schema_editor.execute(
            f"SELECT setval(pg_get_serial_sequence('{table}', 'id'), "  # noqa: S608 — table names from module constant
            f"coalesce(max(id), 1), max(id) IS NOT NULL) FROM {table};"
        )


class Migration(migrations.Migration):
    dependencies = [
        ("django_regional", "0001_squashed_0006_country_default_currency"),
    ]

    operations = [
        migrations.RunPython(reset_pk_sequences, reverse_code=migrations.RunPython.noop),
    ]
