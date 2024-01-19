# Generated by Django 4.2 on 2023-08-20 19:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0006_product_overall_rate"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="product",
            options={"ordering": ["-overall_rate", "product_name"]},
        ),
        migrations.RenameField(
            model_name="product",
            old_name="rate",
            new_name="rate_count",
        ),
    ]