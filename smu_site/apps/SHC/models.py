from django.db import models


class Doc(models.Model):
    doc = models.OneToOneField('documents.Doc',
                               on_delete=models.CASCADE,
                               verbose_name='id документа',
                               primary_key=True)
    description = models.TextField('Описание документа')
    on_changed = models.BigIntegerField('ID заменяемой записи',
                                        null=True)
