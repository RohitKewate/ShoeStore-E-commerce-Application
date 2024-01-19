# Generated by Django 4.2 on 2023-08-18 14:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0003_alter_product_slug"),
        ("account", "0006_alter_profile_profile_image"),
        ("order", "0018_remove_orderitem_status_orderitemhistory"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="orderitemhistory",
            unique_together={("product", "size_varient", "color_varient")},
        ),
        migrations.AddField(
            model_name="orderitemhistory",
            name="customer",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="account.profile",
            ),
        ),
        migrations.AddField(
            model_name="orderitemhistory",
            name="trade_id",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name="orderitemhistory",
            name="order",
        ),
    ]