# Generated by Django 3.2.5 on 2022-10-01 22:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0004_alter_institutiongroup_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='documentquery',
            name='accepted_record',
        ),
        migrations.AlterField(
            model_name='document',
            name='status',
            field=models.CharField(choices=[('CREATED', 'Created'), ('VALIDATING', 'Validating'), ('CLOSED', 'Closed')], default='CREATED', max_length=12),
        ),
        migrations.AlterField(
            model_name='documentquery',
            name='status',
            field=models.CharField(choices=[('CREATED', 'Created'), ('CLOSED', 'Closed')], default='CREATED', max_length=12),
        ),
    ]
