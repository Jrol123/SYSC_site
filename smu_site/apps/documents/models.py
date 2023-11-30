from django.db import models


class Doc(models.Model):
    doc = models.OneToOneField("moderators.Queue",
                               on_delete=models.DO_NOTHING,
                               primary_key=True)
    name = models.CharField("Название документа", max_length=100)
    category = models.CharField("Категория (каталог) документа",
                                max_length=300, default='')
    
    def _img_dir_path(self, filename):
        return (f'documents/{self.category + ("/" if self.category else "")}'
                f'{self.doc}_{filename}')
    
    path = models.FileField("Путь до документа",
                            upload_to=_img_dir_path)
    