# Generated by Django 5.1.7 on 2025-05-08 09:41

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formation', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AnnualHeadcount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('academic_year', models.PositiveIntegerField(help_text="Année de début de l'année universitaire (ex: 2023 pour 2023-2024)")),
                ('students', models.PositiveIntegerField(default=0, help_text="Nombre d'étudiants inscrits pour cette année universitaire")),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_annual_headcounts', to=settings.AUTH_USER_MODEL)),
                ('formation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='annual_headcounts', to='formation.formation')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_annual_headcounts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Annual Headcount',
                'verbose_name_plural': 'Annual Headcounts',
                'db_table': 'annual_headcounts',
                'unique_together': {('formation', 'academic_year')},
            },
        ),
    ]
