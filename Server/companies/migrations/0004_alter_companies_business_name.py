# Generated by Django 3.2.8 on 2021-12-11 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0003_auto_20211206_0236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companies',
            name='business_name',
            field=models.CharField(max_length=255),
        ),
    ]
