# Generated by Django 4.2.6 on 2023-11-30 09:12

from django.db import migrations, models
import django.db.models.deletion
import documents.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('moderators', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Doc',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название документа')),
                ('category', models.CharField(default='', max_length=300, verbose_name='Категория (каталог) документа')),
                ('path', models.FileField(upload_to=documents.models.Doc._img_dir_path, verbose_name='Путь до документа')),
                ('queue', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='moderators.queue')),
            ],
        ),
    ]
