# Generated by Django 4.0 on 2023-11-24 14:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0003_alter_contactleads_superagi_run_complete"),
    ]

    operations = [
        migrations.AddField(
            model_name="contactleads",
            name="superagi_resource",
            field=models.URLField(blank=True, null=True),
        ),
    ]