from django.db import models
from ..moderators.models import Queue


class News(models.Model):
    news_id = models.OneToOneField(Queue, on_delete=models.DO_NOTHING,
                                   to_field="obj_id", primary_key=True)
    title = models.CharField("Заголовок новости", max_length=400)
    text = models.BinaryField("Текст разметки новости")
    # imgs = models.BinaryField("Изображения новости")
    tags = models.TextField("Тэги новости")
    pub_date = models.DateTimeField("Дата и время публикации")


class Event(models.Model):
    event_id = models.OneToOneField(Queue, on_delete=models.DO_NOTHING,
                                    to_field="obj_id", primary_key=True)
    title = models.CharField("Заголовок мероприятия", max_length=400)
    text = models.BinaryField("Текст разметки мероприятия")
    # imgs = models.BinaryField("Изображения новости")
    tags = models.TextField("Тэги мероприятия")
    begin_date = models.DateTimeField("Дата и время начала")
    end_date = models.DateTimeField("Дата и время окончания")
    pub_date = models.DateTimeField("Дата и время публикации")
