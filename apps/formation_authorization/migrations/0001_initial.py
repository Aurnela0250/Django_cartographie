# Generated by Django 5.1.7 on 2025-05-08 01:27

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FormationAuthorization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_debut', models.DateField()),
                ('date_fin', models.DateField(blank=True, null=True)),
                ('status', models.CharField(choices=[('REQUESTED', 'REQUESTED'), ('VALIDATED', 'VALIDATED'), ('REFUSED', 'REFUSED'), ('EXPIRED', 'EXPIRED')], default='REQUESTED', max_length=10)),
                ('arrete', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_formation_authorizations', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_formation_authorizations', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Formation Authorization',
                'verbose_name_plural': 'Formation Authorizations',
                'db_table': 'formation_authorizations',
            },
        ),
    ]
