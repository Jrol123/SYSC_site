from django.db import models


class Queue(models.Model):
    obj_id = models.BigIntegerField("Идентификатор объекта")
    CHOICES = (
        ('doc', 'Документ'),
        ('news', 'Новость'),
        ('event', 'Мероприятие/событие'),
        ('scientist', 'Учёный'),
        ('grant', 'Грант'),
    )
    obj_type = models.CharField("Тип объекта",
                                max_length=10, choices=CHOICES)
    
    class Meta:
        verbose_name = 'Очередь'
        verbose_name_plural = 'Очереди'
        constraints = [
            models.UniqueConstraint(
                fields=['obj_id', 'obj_type'],
                name='unique_obj_id_type'
            )
        ]
