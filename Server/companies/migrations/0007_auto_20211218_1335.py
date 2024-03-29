# Generated by Django 3.2.8 on 2021-12-18 19:35

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('general_ledger', '0002_alter_generalledgercodes_notes'),
        ('companies', '0006_auto_20211214_2206'),
    ]

    operations = [
        migrations.AddField(
            model_name='companies',
            name='accounts_payable_gl',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='accounts_payable_gl_codes_set', to='general_ledger.generalledgercodes'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='companies',
            name='accounts_receivable_gl',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='accounts_receivable_gl_codes_set', to='general_ledger.generalledgercodes'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='companies',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='companies',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
