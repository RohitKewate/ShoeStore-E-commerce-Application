# Generated by Django 4.2 on 2023-08-15 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0003_remove_profile_phone_number_address_phone_number_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="address",
            name="default",
            field=models.BooleanField(default=False),
        ),
    ]