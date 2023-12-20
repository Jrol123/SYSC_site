from django.contrib.auth.models import User
from django.db import models
# from SYSC_site.smu_site.tgbot.auto_dispatch import bot, channel_id


class News(models.Model):
    queue = models.OneToOneField("moderators.Queue",
                                 on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField("Заголовок новости", max_length=400)
    text = models.TextField("Текст разметки новости")
    pub_date = models.DateTimeField("Дата и время публикации",
                                    auto_now_add=True)
    link = models.URLField("Ссылка на новость в телеграм", null=True)

    def __str__(self):
        return (f"News(id={self.id}, user=\"{self.user.username}\", "
                f"title=\"{self.title}\", pub_date={self.pub_date})")

    def get_template_message(self):
        return f"<b>{self.title}</b>\n{self.text}"

    # def delete(self, using=None, keep_parents=False):
    #     bot.delete_message(channel_id, int(self.link.split('/')[-1]))
    #     super().delete(using, keep_parents)


class Event(models.Model):
    queue = models.OneToOneField("moderators.Queue",
                                 on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField("Заголовок мероприятия", max_length=400)
    text = models.TextField("Текст разметки мероприятия")
    begin_date = models.DateTimeField("Дата и время начала")
    end_date = models.DateTimeField("Дата и время окончания")
    pub_date = models.DateTimeField("Дата и время публикации",
                                    auto_now_add=True)
    link = models.URLField("Ссылка на новость в телеграм", null=True)

    def __str__(self):
        return (f"Event(id={self.id}, "
                f"user=\"{self.user.username}\", "
                f"title=\"{self.title}\", pub_date={self.pub_date}), "
                f"begin_date={self.begin_date}, "
                f"end_date={self.end_date}")

    def get_template_message(self):
        return (f"<b>{self.title}</b>\n\n"
                f"Дата начала: {self.begin_date}\n"
                f"Дата окончания: {self.end_date}\n{self.text}")

    # def delete(self, using=None, keep_parents=False):
    #     bot.delete_message(channel_id, int(self.link.split('/')[-1]))
    #     super().delete(using, keep_parents)


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
                             null=True, blank=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE,
                              null=True, blank=True)
    institute = models.ForeignKey("info.Institute",
                                  on_delete=models.CASCADE,
                                  null=True, blank=True)
    scientist = models.ForeignKey("info.Scientist",
                                  on_delete=models.CASCADE,
                                  null=True, blank=True)
    grant = models.ForeignKey("info.Grant", on_delete=models.CASCADE,
                              null=True, blank=True)
    
    def _img_dir_path(self, filename):
        folder = ['news', 'events', 'institutes',
                  'scientists', 'grants']
        cd = lambda: [(i, v) for i, v
                      in enumerate((self.news, self.event,
                                    self.institute, self.scientist,
                                    self.grant)) if v]
        
        return (f'images/{folder[cd()[0][0]]}/{cd()[0][1].id}'
                f'/{filename}')
    
    url_path = models.ImageField("Путь к изображению",
                                 upload_to=_img_dir_path)
    alt = models.CharField("Краткое описание",
                           max_length=400, default='')
    
    def __str__(self):
        return (f"Image(id={self.id}, url_path=\"{self.url_path}\", "
                f"alt=\"{self.alt}\")")
    
    @classmethod
    def get_related_images(cls, obj_id, category):
        assert category in ('news', 'event', 'institute',
                            'scientist', 'grant')
        
        kwargs = {category + '_id': obj_id}
        return list(cls.objects.filter(**kwargs).order_by("id"))
