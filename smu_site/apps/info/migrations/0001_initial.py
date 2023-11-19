# Generated by Django 4.2.6 on 2023-11-19 01:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Grant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Описание гранта')),
            ],
        ),
        migrations.CreateModel(
            name='Institute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500, verbose_name='Название института')),
                ('info', models.TextField(verbose_name='Информация об институте')),
            ],
        ),
        migrations.CreateModel(
            name='ScientistInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Имя учёного')),
                ('position', models.CharField(max_length=300, verbose_name='Позиция учёного')),
                ('degree', models.CharField(max_length=200, verbose_name='Учёная степень')),
                ('links', models.TextField(null=True, verbose_name='Ссылки на учёного')),
                ('institute_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='info.institute')),
            ],
        ),
    ]