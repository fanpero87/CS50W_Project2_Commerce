# Generated by Django 3.0.8 on 2020-07-17 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_auto_20200717_1537'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionitems',
            name='category',
            field=models.CharField(choices=[('ART', 'Art'), ('CAR', 'Cars'), ('CLO', 'Cloths'), ('ELE', 'Electronics'), ('FAS', 'Fashion'), ('MAN', 'Manuscript'), ('TOY', 'Toys')], default=('CHO', 'Choose One'), max_length=3),
        ),
    ]