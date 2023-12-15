# Generated by Django 4.2.6 on 2023-12-14 09:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0001_initial'),
        ('SHC', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Doc',
            fields=[
                ('doc', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='documents.doc', verbose_name='id документа')),
                ('description', models.TextField(verbose_name='Описание документа')),
            ],
        ),
        migrations.RemoveField(
            model_name='blockconnection',
            name='connect_type',
        ),
        migrations.RemoveField(
            model_name='blockconnection',
            name='main_block',
        ),
        migrations.RemoveField(
            model_name='blockconnection',
            name='side_block',
        ),
        migrations.RemoveField(
            model_name='blocklink',
            name='block',
        ),
        migrations.RemoveField(
            model_name='blocklink',
            name='doc',
        ),
        migrations.RemoveField(
            model_name='blocktype',
            name='form',
        ),
        migrations.DeleteModel(
            name='Block',
        ),
        migrations.DeleteModel(
            name='BlockConnection',
        ),
        migrations.DeleteModel(
            name='BlockForm',
        ),
        migrations.DeleteModel(
            name='BlockLink',
        ),
        migrations.DeleteModel(
            name='BlockType',
        ),
        migrations.DeleteModel(
            name='ConnectionType',
        ),
    ]
