# Generated by Django 3.2.5 on 2023-09-12 22:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0014_campaign_institution_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='institution',
            name='metadata',
            field=models.JSONField(default=dict),
        ),
    ]
