# Generated by Django 3.2.5 on 2021-11-21 14:55

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
                ('template', models.JSONField()),
                ('status', models.CharField(choices=[('CREATED', 'Created'), ('INITIALIZED', 'Initialized'), ('VALIDATING', 'Validating'), ('CLOSED', 'Closed')], default='CREATED', max_length=12)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.JSONField(default=dict)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('NONE', 'None'), ('VALIDATING', 'Validating'), ('CLOSED', 'Closed')], default='NONE', max_length=12)),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='campaigns.campaign')),
            ],
        ),
        migrations.CreateModel(
            name='OutputField',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('widget', models.CharField(max_length=64)),
                ('answers', django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), blank=True, null=True, size=None)),
                ('metadata', models.JSONField(blank=True, default=dict)),
                ('type', models.CharField(max_length=10)),
                ('validation', models.BooleanField(default=False)),
                ('default_answer', models.IntegerField(blank=True, default=None, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Query',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField()),
                ('name', models.CharField(max_length=20)),
                ('data', models.JSONField(default=dict)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='queries', to='campaigns.campaign')),
                ('output_field', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='campaigns.outputfield')),
            ],
            options={
                'ordering': ('order',),
            },
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('type', models.CharField(choices=[('NONE', 'None'), ('USER', 'User'), ('FILE', 'File')], default='NONE', max_length=12)),
            ],
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.TextField()),
                ('probability', models.FloatField()),
                ('status', models.CharField(choices=[('NONE', 'None'), ('ACCEPTED', 'Accepted'), ('REJECTED', 'Rejected')], default='NONE', max_length=10)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='records', to='campaigns.document')),
                ('query', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='records', to='campaigns.query')),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='campaigns.source')),
            ],
        ),
        migrations.CreateModel(
            name='DocumentDataField',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('widget', models.CharField(max_length=64)),
                ('type', models.CharField(max_length=10)),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='document_fields', to='campaigns.campaign')),
            ],
        ),
        migrations.AddField(
            model_name='document',
            name='source',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='campaigns.source'),
        ),
        migrations.CreateModel(
            name='UserSource',
            fields=[
                ('source_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='campaigns.source')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='source', to=settings.AUTH_USER_MODEL)),
            ],
            bases=('campaigns.source',),
        ),
        migrations.CreateModel(
            name='FileSource',
            fields=[
                ('source_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='campaigns.source')),
                ('description', models.TextField(blank=True, default='')),
                ('file', models.FileField(upload_to='resources')),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='file_sources', to='campaigns.campaign')),
            ],
            bases=('campaigns.source',),
        ),
    ]
