# Generated by Django 4.2.6 on 2023-12-07 04:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='text',
            field=models.TextField(verbose_name='Текст разметки мероприятия'),
        ),
        migrations.AlterField(
            model_name='news',
            name='text',
            field=models.TextField(verbose_name='Текст разметки новости'),
        ),
    ]
