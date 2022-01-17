# Generated by Django 3.2.8 on 2022-01-02 22:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0002_alter_images_image'),
        ('companies', '0011_alter_companyinvitelist_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='companies',
            name='documents',
            field=models.ManyToManyField(blank=True, related_name='company_documents_set', to='documents.Documents'),
        ),
        migrations.AddField(
            model_name='companies',
            name='images',
            field=models.ManyToManyField(blank=True, related_name='company_images_set', to='documents.Images'),
        ),
    ]
