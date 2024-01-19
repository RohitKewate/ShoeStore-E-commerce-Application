# Generated by Django 4.2 on 2023-08-15 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0004_address_default"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="bio",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="profile",
            name="location",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name="profile",
            name="profile_image",
            field=models.ImageField(default="profiles/avatar.svg", upload_to="profile"),
        ),
    ]
