# Generated by Django 3.2.8 on 2022-01-02 22:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('documents', '0002_alter_images_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='documents',
            name='uploaded_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.RESTRICT, to='accounts.user'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='images',
            name='uploaded_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.RESTRICT, to='accounts.user'),
            preserve_default=False,
        ),
    ]