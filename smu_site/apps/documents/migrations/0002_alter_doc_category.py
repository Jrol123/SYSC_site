# Generated by Django 4.2.6 on 2023-12-12 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doc',
            name='category',
            field=models.CharField(default='unsorted', max_length=300, verbose_name='Категория (каталог) документа'),
        ),
    ]