from django.contrib.auth.models import User
from django.db import models


class News(models.Model):
    news = models.OneToOneField("moderators.Queue",
                                on_delete=models.DO_NOTHING,
                                primary_key=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING,
                             to_field='id')
    title = models.CharField("Заголовок новости", max_length=400)
    text = models.BinaryField("Текст разметки новости")
    pub_date = models.DateTimeField("Дата и время публикации",
                                    auto_now_add=True)
    link = models.URLField("Ссылка на новость в телеграм", null=True)
    
    def __str__(self):
        return (f"News(id={self.news}, user=\"{self.user.username}\", "
                f"title=\"{self.title}\", pub_date={self.pub_date})")


class Event(models.Model):
    event = models.OneToOneField("moderators.Queue",
                                 on_delete=models.DO_NOTHING,
                                 primary_key=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING,
                             to_field='id')
    title = models.CharField("Заголовок мероприятия", max_length=400)
    text = models.BinaryField("Текст разметки мероприятия")
    begin_date = models.DateTimeField("Дата и время начала")
    end_date = models.DateTimeField("Дата и время окончания")
    pub_date = models.DateTimeField("Дата и время публикации",
                                    auto_now_add=True)
    link = models.URLField("Ссылка на новость в телеграм", null=True)
    
    def __str__(self):
        return (f"Event(id={self.event}, "
                f"user=\"{self.user.username}\", "
                f"title=\"{self.title}\", pub_date={self.pub_date}), "
                f"begin_date={self.begin_date}, "
                f"end_date={self.end_date}")


class Image(models.Model):
    """
    0) Пользователь открывает форму.
       в таблице <тип (news, events)> инициализируется статья.
       В коде инициализируется переменная num_images = 0.
    1) Пользователь нажимает на кнопку. Появляется modal
       и в него он загружает картинку и пишет ей название (alt)
       (добавление названия опционально, пользователь не обязан
       всегда его писать. В таком случае просто как название файла
       на сервере)
    2) В папку images/<тип (news, events)>/<id объекта>/
       <переменная num_image>
       прилетает загруженная пользователем картинка
    3) В таблице images создаётся запись под картинку
    4) Переменная num_image увеличивается на 1
    """
    news = models.ForeignKey(News, on_delete=models.CASCADE,
                             # to_field="news",
                             null=True, blank=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE,
                              # to_field="event",
                              null=True, blank=True)
    institute = models.ForeignKey("info.Institute",
                                  on_delete=models.CASCADE,
                                  # to_field="id",
                                  null=True, blank=True)
    scientist = models.ForeignKey("info.ScientistInfo",
                                  on_delete=models.CASCADE,
                                  # to_field="scientist",
                                  null=True, blank=True)
    grant = models.ForeignKey("info.Grant", on_delete=models.CASCADE,
                              # to_field="grant",
                              null=True, blank=True)
    
    def _img_dir_path(self, filename):
        folder = ['news', 'events', 'institutes',
                  'scientists', 'grants']
        cd = lambda: [(i, v) for i, v
                      in enumerate((self.news, self.event,
                                    self.institute, self.scientist,
                                    self.grant)) if v]
        
        return (f'images/{folder[cd()[0][0]]}/{cd()[0][1]}'
                f'/{self.id}_{filename}')
    
    url_path = models.ImageField("Путь к изображению",
                                 upload_to=_img_dir_path)
    alt = models.CharField("Краткое описание",
                           max_length=400, default='')
    
    def __str__(self):
        return (f"Image(id={self.id}, url_path=\"{self.url_path}\", "
                f"alt=\"{self.alt}\")")
