# Generated by Django 3.0.8 on 2020-07-16 19:23

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_auto_20200716_1753'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctionitems',
            name='date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
