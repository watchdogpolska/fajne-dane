# Generated by Django 3.2.5 on 2023-07-30 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0012_filesource_raw_report'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filesource',
            name='raw_report',
            field=models.JSONField(default=dict),
        ),
        migrations.AlterField(
            model_name='filesource',
            name='status',
            field=models.CharField(choices=[('CREATED', 'Created'), ('PROCESSING', 'Processing'), ('FINISHED', 'Finished'), ('FAILED', 'Failed')], default='CREATED', max_length=12),
        ),
    ]
