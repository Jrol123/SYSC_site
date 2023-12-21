from django.contrib.auth.models import User
from django.db import models


class Institute(models.Model):
    name = models.CharField("Название института",
                            max_length=400, unique=True)
    description = models.TextField("Информация об институте",
                                   default="None", blank=True)
    employees_count = models.IntegerField("Число сотрудников",
                                          default=1)
    scientist_count = models.IntegerField("Число молодых учёных",
                                          default=0)
    chairman = models.CharField("Ф.И.О. председателя СМУ",
                                max_length=200)
    link = models.URLField("Ссылка на сайт института")
    smu_link = models.URLField("Ссылка на сайт СМУ института",
                               null=True, blank=True)
    on_changed = models.BigIntegerField('ID заменяемой записи',
                                        null=True)
    
    def __str__(self):
        return (f"Institute(id={self.id}, name=\"{self.name}\", "
                f"info=\"{self.description[:50]}...\", "
                f"link=\"{self.link}\")")


class Scientist(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    queue = models.OneToOneField("moderators.Queue",
                                 on_delete=models.SET_NULL, null=True)
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE,
                                  null=True)
    name = models.CharField("Имя учёного", max_length=200)
    lab = models.CharField("Лаборатория", max_length=300)
    position = models.CharField("Должность", max_length=300)
    degree = models.CharField("Учёная степень", max_length=200,
                              null=True)
    scientific_interests = models.TextField("Сфера научных интересов")
    on_changed = models.BigIntegerField('ID заменяемой записи',
                                        null=True)
    
    def __str__(self):
        return (f"ScientistInfo(id={self.id}, "
                f"institute=\"{self.institute.name}\", "
                f"name=\"{self.name}\", position=\"{self.position}\", "
                "scientific_interests="
                f"\"{self.scientific_interests}\")")


class ScientistLink(models.Model):
    scientist = models.ForeignKey(Scientist,
                                  on_delete=models.CASCADE)
    link = models.URLField("Ссылка на профиль")
    service_name = models.CharField("Краткое описание", max_length=250)


class Grant(models.Model):
    queue = models.OneToOneField("moderators.Queue",
                                 on_delete=models.SET_NULL, null=True)
    name = models.CharField("Название гранта", max_length=300)
    description = models.TextField("Описание гранта", null=True)
    end_doc_date = models.DateTimeField("Дата окончания приёма заявок",
                                        null=True)
    end_result_date = models.DateTimeField("Дата подведения итогов",
                                           null=True)
    criteria = models.TextField("Критерии к участникам", null=True)
    link = models.URLField("Ссылка на страницу с грантом")
    
    def __str__(self):
        return (f"Grant(id={self.id}, name=\"{self.name}\", "
                f"end_doc_date=\"{self.end_doc_date}\", "
                f"end_result_date=\"{self.end_result_date}\")")
