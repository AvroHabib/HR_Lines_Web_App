# Generated by Django 5.1.1 on 2024-11-25 11:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ml_model', '0022_bes_operator_schedule_operator'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bes_complete',
            old_name='atb_cpg',
            new_name='atb_cgp',
        ),
    ]
