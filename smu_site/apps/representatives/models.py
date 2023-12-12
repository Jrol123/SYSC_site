from django.db import models
from django.contrib.auth.models import User


class ReprInst(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name="Представитель")
    institute = models.ForeignKey("info.Institute",
                                  on_delete=models.DO_NOTHING,
                                  verbose_name="Представитель")
