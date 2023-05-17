# Generated by Django 4.2.1 on 2023-05-16 09:34

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ServiceRecord",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("datetime", models.DateTimeField()),
                ("description", models.TextField()),
                ("service_state", models.IntegerField(default=0)),
            ],
            options={
                "db_table": "service_record",
            },
        ),
        migrations.CreateModel(
            name="ServiceType",
            fields=[
                (
                    "service_type_id",
                    models.AutoField(primary_key=True, serialize=False),
                ),
                ("name", models.CharField(max_length=100)),
            ],
            options={
                "db_table": "service_type",
            },
        ),
    ]
