# Generated by Django 3.2.5 on 2023-09-03 11:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0013_auto_20230730_2158'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='institution_group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='campaigns', to='campaigns.institutiongroup'),
        ),
    ]
