# Generated by Django 3.2.8 on 2022-01-09 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0003_alter_notes_user'),
        ('contacts', '0002_auto_20211218_2328'),
    ]

    operations = [
        migrations.AddField(
            model_name='addresses',
            name='notes',
            field=models.ManyToManyField(blank=True, related_name='address_notes_set', to='notes.Notes'),
        ),
        migrations.AddField(
            model_name='contacts',
            name='notes',
            field=models.ManyToManyField(blank=True, related_name='contacts_notes_set', to='notes.Notes'),
        ),
    ]
