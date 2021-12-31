# Generated by Django 3.2.8 on 2021-11-20 18:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('general_ledger', '0002_alter_generalledgercodes_notes'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contacts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Companies',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('business_name', models.CharField(blank=True, max_length=255)),
                ('legal_name', models.CharField(blank=True, max_length=255)),
                ('business_address', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='companies_business_address_set', to='contacts.addresses')),
                ('contacts', models.ManyToManyField(blank=True, related_name='company_contacts_set', to='contacts.Contacts')),
                ('gl_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company_gl_codes_set', to='general_ledger.generalledgercodes')),
                ('mailing_address', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='companies_mailing_address_set', to='contacts.addresses')),
                ('users', models.ManyToManyField(blank=True, related_name='company_user_set', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
