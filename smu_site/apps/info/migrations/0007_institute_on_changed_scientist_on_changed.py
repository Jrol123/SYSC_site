# Generated by Django 4.2.6 on 2023-12-21 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0006_remove_scientist_achievements_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='institute',
            name='on_changed',
            field=models.BigIntegerField(null=True, verbose_name='ID заменяемой записи'),
        ),
        migrations.AddField(
            model_name='scientist',
            name='on_changed',
            field=models.BigIntegerField(null=True, verbose_name='ID заменяемой записи'),
        ),
    ]
