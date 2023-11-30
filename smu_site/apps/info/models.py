from django.db import models


class Institute(models.Model):
    name = models.CharField("Название института", max_length=400)
    description = models.TextField("Информация об институте")
    structure = models.TextField("Структура института")
    link = models.URLField("Ссылка на сайт института")
    
    def __str__(self):
        return (f"Institute(id={self.id}, name=\"{self.name}\", "
                f"info=\"{self.description[:50]}...\", "
                f"link=\"{self.link}\")")


class ScientistInfo(models.Model):
    scientist = models.OneToOneField("moderators.Queue",
                                     on_delete=models.DO_NOTHING,
                                     primary_key=True)
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE,
                                  null=True)
    name = models.CharField("Имя учёного", max_length=200)
    lab = models.CharField("Лаборатория", max_length=300)
    position = models.CharField("Должность", max_length=300)
    degree = models.CharField("Учёная степень", max_length=200,
                              null=True)
    teaching_info = models.TextField("Информация о преподавании",
                                     null=True)
    scientific_interests = models.TextField("Сфера научных интересов")
    achievements = models.TextField("Достижения", null=True)
    future_plans = models.TextField("Планы на будущее", null=True)
    
    def __str__(self):
        return (f"ScientistInfo(id={self.scientist}, "
                f"institute=\"{self.institute.name}\", "
                f"name=\"{self.name}\", position=\"{self.position}\", "
                "scientific_interests="
                f"\"{self.scientific_interests}\")")


class ScientistLink(models.Model):
    scientist = models.ForeignKey(ScientistInfo,
                                  on_delete=models.CASCADE,
                                  to_field="scientist")
    link = models.URLField("Ссылка на профиль")
    service_name = models.CharField("Краткое описание", max_length=250)


class ScientistPublication(models.Model):
    scientist = models.ForeignKey(ScientistInfo,
                                  on_delete=models.CASCADE,
                                  to_field="scientist")
    pub_link = models.TextField("Ссылка на публикацию")
    

class Grant(models.Model):
    grant = models.OneToOneField("moderators.Queue",
                                 on_delete=models.DO_NOTHING,
                                 primary_key=True)
    name = models.CharField("Название гранта", max_length=300)
    description = models.TextField("Описание гранта", null=True)
    end_doc_date = models.DateTimeField("Дата окончания приёма заявок",
                                        null=True)
    end_result_date = models.DateTimeField("Дата подведения итогов",
                                           null=True)
    criteria = models.TextField("Критерии к участникам")
    link = models.URLField("Ссылка на страницу с грантом")
    
    def __str__(self):
        return (f"Grant(id={self.grant}, name=\"{self.name}\", "
                f"end_doc_date=\"{self.end_doc_date}\", "
                f"end_result_date=\"{self.end_result_date}\")")

