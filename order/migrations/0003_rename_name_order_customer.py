# Generated by Django 4.2 on 2023-07-24 10:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("order", "0002_order_complete"),
    ]

    operations = [
        migrations.RenameField(
            model_name="order",
            old_name="name",
            new_name="customer",
        ),
    ]
