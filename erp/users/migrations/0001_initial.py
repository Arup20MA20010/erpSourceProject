# Generated by Django 4.1.7 on 2023-04-05 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('erpApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rollNo', models.CharField(max_length=9)),
                ('name', models.CharField(max_length=100)),
                ('CourseId', models.ManyToManyField(related_name='students', to='erpApp.course')),
            ],
        ),
    ]
