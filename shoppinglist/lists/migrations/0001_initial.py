# Generated by Django 5.1.4 on 2025-01-18 08:20

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ListCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_budget', models.IntegerField(blank=True, null=True)),
                ('category_name', models.CharField(blank=True, max_length=255)),
                ('archived_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('archived_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category_owner_archiver', to=settings.AUTH_USER_MODEL)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category_owner_creator', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category_owner_modifier', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ListIndividual',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('individual_budget', models.IntegerField(blank=True, null=True)),
                ('archived_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('notes', models.CharField(blank=True, max_length=255)),
                ('image', models.URLField(blank=True, null=True)),
                ('archived_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='list_owner_archiver', to=settings.AUTH_USER_MODEL)),
                ('category_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='list_category', to='lists.listcategory')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='list_owner_creator', to=settings.AUTH_USER_MODEL)),
                ('list_owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='list_owner', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='list_owner_modifier', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
