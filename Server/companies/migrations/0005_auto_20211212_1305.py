# Generated by Django 3.2.8 on 2021-12-12 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0004_alter_companies_business_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='companies',
            options={'ordering': ('business_name',), 'verbose_name': 'Company', 'verbose_name_plural': 'Companies'},
        ),
        migrations.AlterModelOptions(
            name='companyinvitelist',
            options={'ordering': ('email',), 'verbose_name': 'Company Invite List', 'verbose_name_plural': 'Company Invites List'},
        ),
        migrations.RenameField(
            model_name='companies',
            old_name='allowed_users',
            new_name='allowed_admins',
        ),
        migrations.AlterField(
            model_name='companies',
            name='business_name',
            field=models.CharField(default=None, max_length=255),
        ),
    ]
