# Generated by Django 4.2.6 on 2023-11-30 05:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='scientistlink',
            old_name='scientist_id',
            new_name='scientist',
        ),
        migrations.RenameField(
            model_name='scientistpublication',
            old_name='scientist_id',
            new_name='scientist',
        ),
    ]
