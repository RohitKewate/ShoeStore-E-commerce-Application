# Generated by Django 4.2 on 2023-07-24 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("order", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="complete",
            field=models.BooleanField(default=False, null=True),
        ),
    ]
