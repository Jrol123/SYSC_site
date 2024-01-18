from django.db import models


class Queue(models.Model):
    CHOICES = (
        ('doc', 'Документ'),
        ('news', 'Новость'),
        ('event', 'Мероприятие/событие'),
        ('scientist', 'Учёный')
    )
    obj_type = models.CharField("Тип объекта",
                                max_length=10, choices=CHOICES)
    
    SCHOICES = (
        ('pub', 'Публикация'),
        ('chg', 'Изменение'),
        ('del', 'Удаление')
    )
    status = models.CharField("Статус запрашиваемого объекта",
                              max_length=10, choices=SCHOICES,
                              default='Публикация')
    
    class Meta:
        verbose_name = 'Очередь'
        verbose_name_plural = 'Очереди'
