# Generated by Django 4.1.7 on 2023-04-05 15:04

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import erpApp.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('departmentName', models.CharField(max_length=100)),
                ('facId', models.IntegerField()),
                ('depCode', models.CharField(max_length=2, validators=[erpApp.models.depError])),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('courseName', models.CharField(max_length=50)),
                ('credits_score', models.IntegerField(validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(1)])),
                ('deptId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dept', to='erpApp.department')),
            ],
        ),
    ]