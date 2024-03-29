# Generated by Django 3.2.8 on 2021-12-01 02:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0001_initial'),
        ('notes', '0002_auto_20211130_2020'),
        ('companies', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='companies',
            name='users',
        ),
        migrations.AddField(
            model_name='companies',
            name='notes',
            field=models.ManyToManyField(blank=True, related_name='company_notes_set', to='notes.Notes'),
        ),
        migrations.AlterField(
            model_name='companies',
            name='business_address',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='company_business_address_set', to='contacts.addresses'),
        ),
        migrations.AlterField(
            model_name='companies',
            name='mailing_address',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='company_mailing_address_set', to='contacts.addresses'),
        ),
    ]
