# Generated by Django 2.1.7 on 2019-05-06 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0030_game_by_create'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='super_edititems',
            field=models.BooleanField(default=False),
        ),
    ]