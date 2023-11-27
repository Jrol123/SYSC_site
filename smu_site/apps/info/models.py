from django.db import models


class Institute(models.Model):
    name = models.CharField("Название института", max_length=500)
    info = models.TextField("Информация об институте")


class ScientistInfo(models.Model):
    scientist_id = models.OneToOneField("moderators.Queue",
                                        on_delete=models.DO_NOTHING,
                                        primary_key=True)
    institute = models.ForeignKey(Institute,
                                  on_delete=models.CASCADE, null=True)
    name = models.CharField("Имя учёного", max_length=200)
    position = models.CharField("Позиция учёного", max_length=300)
    degree = models.CharField("Учёная степень", max_length=200)
    links = models.TextField("Ссылки на учёного", null=True)


class Grant(models.Model):
    grant_id = models.OneToOneField("moderators.Queue",
                                    on_delete=models.DO_NOTHING,
                                    primary_key=True)
    name = models.CharField("Название гранта",
                            max_length=300, default="")
    description = models.TextField("Описание гранта", null=True)
    end_doc_date = models.DateTimeField("Дата окончания приёма заявок",
                                        null=True)
    end_result_date = models.DateTimeField("Дата подведения итогов",
                                           null=True)

