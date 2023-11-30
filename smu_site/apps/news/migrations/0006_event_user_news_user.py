# Generated by Django 4.2.6 on 2023-11-27 04:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('news', '0005_remove_event_tags_remove_news_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='user',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='news',
            name='user',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]