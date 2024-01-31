from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField("Название категории", max_length=300)


class Doc(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    queue = models.OneToOneField("moderators.Queue",
                                 on_delete=models.SET_NULL, null=True)
    name = models.CharField("Название документа", max_length=100)

    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 null=True)
    
    def _img_dir_path(self, filename):
        return (f'documents/'
                f'{self.category.name}'
                f'/{filename}')
    
    path = models.FileField("Путь до документа",
                            upload_to=_img_dir_path)
    