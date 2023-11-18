from django.db import models
from ..moderators.models import Queue


class Doc(models.Model):
    doc_id = models.OneToOneField(Queue, on_delete=models.DO_NOTHING,
                                  on_field="obj_id", primary_key=True)
    name = models.FileField("Название документа", max_length=100)
    path = models.FilePathField("Путь до документа", max_length=200)
