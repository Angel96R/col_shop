# Generated by Django 2.1.7 on 2019-05-14 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0044_auto_20190511_2120'),
    ]

    operations = [
        migrations.AddField(
            model_name='check',
            name='completed_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]