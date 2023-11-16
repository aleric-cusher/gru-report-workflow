# Generated by Django 4.0 on 2023-11-16 08:32

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ContactLeads",
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
                ("name", models.CharField(max_length=60)),
                ("email", models.EmailField(blank=True, max_length=254, null=True)),
                ("phone", models.CharField(max_length=15)),
                ("message", models.CharField(blank=True, max_length=300, null=True)),
                ("company_name", models.CharField(max_length=50)),
                ("company_website", models.URLField()),
                ("industry", models.CharField(max_length=20)),
                ("goals", models.CharField(max_length=200)),
            ],
        ),
    ]
