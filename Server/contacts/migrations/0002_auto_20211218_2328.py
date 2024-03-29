# Generated by Django 3.2.8 on 2021-12-19 05:28

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contacts',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='contacts',
            name='phone_1',
            field=models.CharField(blank=True, max_length=10, validators=[django.core.validators.RegexValidator('^\\d{10}$', code='invalid-phone', message='Invalid phone number. Should be 10 digits')]),
        ),
        migrations.AlterField(
            model_name='contacts',
            name='phone_2',
            field=models.CharField(blank=True, max_length=10, validators=[django.core.validators.RegexValidator('^\\d{10}$', code='invalid-phone', message='Invalid phone number. Should be 10 digits')]),
        ),
    ]
