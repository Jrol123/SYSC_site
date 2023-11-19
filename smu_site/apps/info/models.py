from django.db import models


class Institute(models.Model):
    name = models.CharField("Название института", max_length=500)
    info = models.TextField("Информация об институте")


class ScientistInfo(models.Model):
    institute = models.ForeignKey(Institute,
                                  on_delete=models.CASCADE, null=True)
    name = models.CharField("Имя учёного", max_length=200)
    position = models.CharField("Позиция учёного", max_length=300)
    degree = models.CharField("Учёная степень", max_length=200)
    links = models.TextField("Ссылки на учёного", null=True)


class Grant(models.Model):
    text = models.TextField("Описание гранта")
