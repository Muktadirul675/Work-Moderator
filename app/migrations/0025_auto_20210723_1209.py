# Generated by Django 3.1 on 2021-07-23 06:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0024_auto_20210723_1200'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='work',
            name='project',
        ),
        migrations.DeleteModel(
            name='File',
        ),
        migrations.DeleteModel(
            name='Work',
        ),
    ]
