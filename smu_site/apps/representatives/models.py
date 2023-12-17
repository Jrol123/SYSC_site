from django.contrib.auth.models import User
from django.db import models


class ReprInst(models.Model):
    institute = models.ForeignKey("info.Institute",
                                  on_delete=models.CASCADE,
                                  verbose_name="id института")
    user = models.OneToOneField(User, on_delete=models.CASCADE)
