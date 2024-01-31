import configparser
from html.parser import HTMLParser
import re
import telebot
import time
from telebot import types

# Нужно для импорта из приложений проекта
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'smu_site.settings')
import django
django.setup()

# Тот самый импорт, для которого нужна вся конструкция выше
from django.conf import settings
from news.models import News, Event, Image


"""
SYSC_site/
    __init__.py
    smu_site/
        __init__.py
        settings.py
        tgbot/
            auto_bot.py
        apps/
            __init__.py
            news/
                __init__.py
                models.py
"""


bot = telebot.TeleBot(
    token="6933728312:AAEovNd1s3kIm75O0LKgu90DLqJ3uxyCpTg")
channel_id = -1001935648024
link_temp = "https://t.me/c/1935648024/"

cfg = configparser.ConfigParser()
cfg.read("config.cfg", encoding='utf-8')
last_mess_id = int(cfg['Support']['last_message_id'])


def delete(self, using=None, keep_parents=False):
    bot.delete_message(channel_id, int(self.link.split('/')[-1]))
    super().delete(using, keep_parents)


News.delete = delete
Event.delete = delete


def update_conf(field: str, value: str):
    cfg.set("Support", field, value)
    with open('config.cfg', 'w') as configfile:
        cfg.write(configfile)


class MyHTMLParser(HTMLParser):
    def __init__(self, allowed_tags):
        super().__init__()
        self.allowed_tags = allowed_tags
        self.result = []

    def handle_starttag(self, tag, attrs):
        if tag in self.allowed_tags:
            self.result.append(f"<{tag}>")

    def handle_endtag(self, tag):
        if tag in self.allowed_tags:
            self.result.append(f"</{tag}>")

    def handle_data(self, data):
        self.result.append(data)


def clear_message(text):
    # сохраняем только указанные теги
    allowed_tags = ["p", "a", "b", "strong", "i", "em", "u", "ins", "s",
                    "strike", "del", "code", "pre"]
    parser = MyHTMLParser(allowed_tags)
    print('before', text)
    parser.feed(text)
    print('after', ''.join(parser.result))
    return ''.join(parser.result)


def split_text(text, limit) -> list[str] or str:
    if len(text) < limit:
        return text
    
    # разделение по переносам строки
    if '\n' in text:
        text = text.split('\n')
        i = 0
        while i < len(text) - 1:
            while (i < len(text) - 1
                   and len(text[i] + text[i + 1]) < limit):
                text[i] += ('\n' + text[i + 1])
                del text[i + 1]
            
            i += 1
    
    # разделение по пробелам
    if (isinstance(text, list) and
       any((len(t) > limit and ' ' in t) for t in text)):
        i = 0
        for j in range(len(text)):
            if len(text[j]) > limit:
                i = j
                break
        
        # часть текста, разделённая пробелами
        text2 = text[i:]
        del text[i:]
        
        # делаем список слов
        text2 = (' '.join(text2)).split()
        while len(text2):
            while 1 < len(text2) and len(text2[0] + text2[1]) < limit:
                text2[0] += (' ' + text2[1])
                del text2[1]
            
            text.append(text2[0])
            del text2[0]
        
        del text2
    elif isinstance(text, str):
        text = text.split()
        i = 0
        while i < len(text) - 1:
            while (i < len(text) - 1
                   and len(text[i] + text[i + 1]) < limit):
                text[i] += (' ' + text[i + 1])
                del text[i + 1]
            
            i += 1
        
    # разделение по символам
    if any(len(t) > limit for t in text):
        for j in range(len(text)):
            if len(text[j]) > limit:
                tmpt = text[j][limit - 3:]
                text[j] = text[j][:limit - 3] + '...'
                if j + 1 < len(text):
                    text[j + 1] += tmpt
                else:
                    text.append(tmpt)
    
    return text


def split_message(text, limit) -> list[str] or str:
    print('unsplit', text)
    text = text.replace('<p>', '\n').replace('</p>', '\n')
    print('split', text)
    
    text = split_text(text, limit)
    
    # nt = [header] if isinstance(header, str) else header
    # if len(text) > 2:
    #     for i in range(2, len(text)):
    #         if isinstance(text[i], list):
    #             nt.extend(text[i])
    #         else:
    #             nt.append(text[i])
    # else:
    #     return '\n'.join(nt)
    
    return text


def news_mailing(wait_for):
    global last_mess_id
    
    while True:
        time.sleep(wait_for)
        
        nw = list(News.objects.filter(queue_id__isnull=True, link=None)
                  .order_by("pub_date"))
        ev = list(Event.objects.filter(queue_id__isnull=True, link=None)
                  .order_by("pub_date"))
        
        if nw:
            nw = nw[0]
            m = clear_message(nw.get_template_message())
            nwimg = Image.get_related_images(nw.id, 'news')
            if nwimg:
                nwimg = open(settings.MEDIA_ROOT.replace('\\', '/')
                             + '/' + str(nwimg[0].url_path), 'rb')
                if len(m) < 1024:
                    bot.send_photo(channel_id, nwimg,
                                   caption=split_message(m, 1024),
                                   parse_mode='html')
                    
                    last_mess_id += 1
                    nw.link = (link_temp + str(last_mess_id))
                    update_conf("last_message_id",
                                str(last_mess_id))
                    nw.save(update_fields=["link"])
                    
                    update_conf("last_message_id",
                                str(last_mess_id))
                else:
                    m, *sepm = split_message(m, 1024)
                    bot.send_photo(channel_id, nwimg, caption=m,
                                   parse_mode='html')
                    
                    for i in range(len(sepm)):
                        bot.send_message(channel_id, sepm[i],
                                         parse_mode="html")
                        
                    nw.link = (link_temp + str(last_mess_id + 1))
                    last_mess_id += len(sepm) + 1
                    update_conf("last_message_id",
                                str(last_mess_id))
                    nw.save(update_fields=["link"])
                    
            else:
                if len(m) < 4096:
                    bot.send_message(channel_id, split_message(m, 1024),
                                     parse_mode="html")
                    
                    last_mess_id += 1
                    nw.link = (link_temp + str(last_mess_id))
                    update_conf("last_message_id",
                                str(last_mess_id))
                    nw.save(update_fields=["link"])
                else:
                    m = split_message(m, 4096)
                    for i in range(len(m)):
                        bot.send_message(channel_id, m[i],
                                         parse_mode="html")
                    
                    nw.link = (link_temp + str(last_mess_id + 1))
                    last_mess_id += len(m)
                    update_conf("last_message_id",
                                str(last_mess_id))
                    nw.save(update_fields=["link"])
        if ev:
            ev = ev[0]
            m = clear_message(ev.get_template_message())
            evimg = Image.get_related_images(ev.id, 'event')
            if evimg:
                evimg = open(settings.MEDIA_ROOT.replace('\\', '/')
                             + '/' + str(evimg[0].url_path), 'rb')
                if len(m) < 1024:
                    bot.send_photo(channel_id, evimg,
                                   caption=split_message(m, 1024),
                                   parse_mode='html')
                    
                    last_mess_id += 1
                    ev.link = (link_temp + str(last_mess_id))
                    update_conf("last_message_id",
                                str(last_mess_id))
                    ev.save(update_fields=["link"])
                else:
                    m, *sepm = split_message(m, 1024)
                    bot.send_photo(channel_id, evimg, caption=m,
                                   parse_mode='html')
                    
                    for i in range(len(sepm)):
                        bot.send_message(channel_id, sepm[i],
                                         parse_mode="html")
                        
                    last_mess_id += 1
                    ev.link = (link_temp + str(last_mess_id))
                    last_mess_id += len(sepm)
                    update_conf("last_message_id",
                                str(last_mess_id))
                    ev.save(update_fields=["link"])
            else:
                if len(m) < 4096:
                    bot.send_message(channel_id,
                                     split_message(m, 4096),
                                     parse_mode="html")
                    
                    last_mess_id += 1
                    ev.link = (link_temp + str(last_mess_id))
                    update_conf("last_message_id",
                                str(last_mess_id))
                    ev.save(update_fields=["link"])
                else:
                    m = split_message(m, 4096)
                    
                    for i in range(len(m)):
                        bot.send_message(channel_id, m[i],
                                         parse_mode="html")
                    
                    ev.link = (link_temp + str(last_mess_id + 1))
                    last_mess_id += len(m)
                    update_conf("last_message_id",
                                str(last_mess_id))
                    ev.save(update_fields=["link"])


if __name__ == '__main__':
    news_mailing(10)
    bot.infinity_polling(non_stop=True, timeout=60)
