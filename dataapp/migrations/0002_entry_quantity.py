# Generated by Django 5.1.2 on 2024-10-26 01:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
    ]
