# Generated by Django 3.1.1 on 2020-10-01 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sdms_app', '0002_auto_20201001_0859'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feesinfo',
            name='amount',
            field=models.IntegerField(default=0),
        ),
    ]
