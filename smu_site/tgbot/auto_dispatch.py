import configparser
import telebot
import time
from telebot import types

# Нужно для импорта из приложений проекта
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'SYSC_site.smu_site.settings')
import django
django.setup()

# Тот самый импорт, для которого нужна вся конструкция выше
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
    self.delete(using, keep_parents)


News.delete = delete
Event.delete = delete


def update_conf(field: str, value: str):
    cfg.set("Support", field, value)
    with open('config.cfg', 'w') as configfile:
        cfg.write(configfile)


def split_message(text, limit) -> list[str]:
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


def news_mailing(wait_for):
    global last_mess_id
    
    while True:
        print('test')
        
        time.sleep(wait_for)
        
        nw = list(News.objects.filter(queue_id__isnull=True, link=None)
                  .order_by("pub_date"))
        ev = list(Event.objects.filter(queue_id__isnull=True, link=None)
                  .order_by("pub_date"))
        
        if nw:
            nw = nw[0]
            nwmedia = [types.InputMediaPhoto(open(photo, 'rb'))
                       for photo in Image.get_related_images(
                    nw.id, 'news')]
            
            if nwmedia:
                m = nw.get_template_message()
                if len(m) < 1024:
                    nwmedia[0].caption = m
                    nwmedia[0].parse_mode = "html"
                    bot.send_media_group(channel_id, nwmedia)
                    
                    last_mess_id += 1
                    nw.link = (link_temp + str(last_mess_id))
                    update_conf("last_message_id",
                                str(last_mess_id))
                    nw.save(update_fields=["link"])
                    
                    update_conf("last_message_id",
                                str(last_mess_id))
                else:
                    m, *sepm = split_message(m, 1024)
                    nwmedia[0].caption = m
                    nwmedia[0].parse_mode = "html"
                    bot.send_media_group(channel_id, nwmedia)
                    
                    for i in range(len(sepm)):
                        bot.send_message(channel_id, sepm[i],
                                         parse_mode="html")
                        
                    nw.link = (link_temp + str(last_mess_id + 1))
                    last_mess_id += len(sepm) + 1
                    update_conf("last_message_id",
                                str(last_mess_id))
                    nw.save(update_fields=["link"])
                    
            else:
                m = nw.get_template_message()
                if len(m) < 4096:
                    bot.send_message(channel_id, m, parse_mode="html")
                    
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
            evmedia = [types.InputMediaPhoto(open(photo, 'rb'))
                       for photo in Image.get_related_images(
                    ev.id, 'event')]
            
            if evmedia:
                m = ev.get_template_message()
                if len(m) < 1024:
                    evmedia[0].caption = m
                    evmedia[0].parse_mode = "html"
                    bot.send_media_group(channel_id, evmedia)
                    
                    last_mess_id += 1
                    ev.link = (link_temp + str(last_mess_id))
                    update_conf("last_message_id",
                                str(last_mess_id))
                    ev.save(update_fields=["link"])
                else:
                    m, *sepm = split_message(m, 1024)
                    evmedia[0].caption = m
                    evmedia[0].parse_mode = "html"
                    bot.send_media_group(channel_id, evmedia)
                    
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
                m = ev.get_template_message()
                if len(m) < 4096:
                    bot.send_message(channel_id, m, parse_mode="html")
                    
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
