from django.db import models


class Doc(models.Model):
    doc = models.OneToOneField("moderators.Queue",
                               on_delete=models.DO_NOTHING,
                               primary_key=True)
    name = models.FileField("Название документа", max_length=100)
    path = models.FilePathField("Путь до документа", max_length=200)
