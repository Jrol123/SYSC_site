# Generated by Django 4.2.6 on 2023-11-27 02:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_image_grant_image_institute_image_scientist'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='tags',
        ),
        migrations.RemoveField(
            model_name='news',
            name='tags',
        ),
    ]
