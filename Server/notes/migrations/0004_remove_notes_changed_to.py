# Generated by Django 3.2.8 on 2022-01-17 21:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0003_alter_notes_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notes',
            name='changed_to',
        ),
    ]
