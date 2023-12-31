# Generated by Django 4.0 on 2023-11-16 19:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="contactleads",
            name="agent_id",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="contactleads",
            name="run_id",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="contactleads",
            name="superagi_run_complete",
            field=models.BooleanField(blank=True, default=False),
        ),
    ]
