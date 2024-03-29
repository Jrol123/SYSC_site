# Generated by Django 4.2.6 on 2023-12-12 09:13


from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('info', '0003_alter_institute_description_alter_institute_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReprInst',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('institute', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='info.institute', verbose_name='Представитель')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Представитель')),
            ],
        ),
    ]
