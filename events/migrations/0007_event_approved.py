# Generated by Django 4.2.4 on 2023-09-01 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_venue_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='approved',
            field=models.BooleanField(default=False, verbose_name='Approved'),
        ),
    ]
