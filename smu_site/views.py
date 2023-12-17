import os
from bs4 import BeautifulSoup as BS
from datetime import date, timedelta

from django.contrib.auth import authenticate, login
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader
from django.shortcuts import render
from django.utils.timezone import localdate

from .forms import LoginForm
from news.models import News, Event, Image
from info.models import Grant


def index(request):
    # Получаем даты для фильтрации списка новостей
    sdate = date.fromisoformat(
        request.POST.get("start-date", "2023-11-28"))
    edate = date.fromisoformat(
        request.POST.get("end-date", localdate().isoformat()))
    edate += timedelta(days=1)
    
    # Выбираем те новости и события, которые не находятся в очереди
    last_news = News.objects.filter(
        pub_date__range=(sdate, edate), queue_id__isnull=True)
    last_news = [(n, Image.objects.filter(news_id=n.id).first())
                 for n in last_news]
    last_events = Event.objects.filter(
        pub_date__range=(sdate, edate), queue_id__isnull=True)
    last_events = [(e, Image.objects.filter(event_id=e.id).first())
                   for e in last_events]
    last_news += last_events
    
    # Сортируем по дате и выбираем первые 5 для первой страницы новостей
    # в будущем нужно реализовать pagination
    last_news = list(sorted(last_news, key=lambda x: x[0].pub_date,
                            reverse=True))
    
    # функция для сокращения текста
    def trim_text(text: str, limit):
        if len(text) < limit:
            return text
        
        si1 = text.find('. ')
        si2 = text.find('! ')
        si3 = text.find('? ')
        if max(si1, si2, si3) != -1:
            si = min(i for i in (si1, si2, si3) if i != -1)
            if si < limit:
                return text[:si + 2] + trim_text(text[si + 2:],
                                                 limit - si - 1)
        
        if ' ' in text:
            t = ''
            for w in text.split(' '):
                if len(t) + len(w) < limit:
                    t += w + ' '
                else:
                    break
            
            return t + ' ...'
        
        return text[:limit - 3] + '...'
    
    # объединяем со списков месяцев и кратким текстом
    month = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
             'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    last_news = [(n, month[n.pub_date.month - 1],
                  trim_text(BS(n.text, 'html.parser')
                            .select_one('p').text, 280), img)
                 for n, img in last_news]
    
    p = Paginator(last_news, 5)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        # Если page_number не является целым числом, то присваивается 1
        page_obj = p.page(1)
    except EmptyPage:
        # Если страница пустая, возвращает последнюю страницу
        page_obj = p.page(p.num_pages)
    
    # переводим даты в изначальный формат
    sdate = sdate.isoformat()
    edate -= timedelta(days=1)
    edate = edate.isoformat()
    
    # Получаем актуальные события и гранты
    events = (Event.objects.filter(queue_id__isnull=True)
              .order_by('begin_date', '-pub_date'))[:3]
    events = [(e, trim_text(BS(e.text, 'html.parser')
                            .select_one('p').text, 180))
              for e in events]
    grants = (Grant.objects.filter(queue_id__isnull=True)
              .order_by('end_doc_date'))[:3]
    
    return render(request, 'index.html',
                  {
                      "is_moder": request.user.groups
                      .filter(name='moderator').exists(),
                      "is_repr": request.user.groups
                      .filter(name='representative').exists(),
                      "last_news": page_obj,
                      "sdate": sdate,
                      "edate": edate,
                      "events": events,
                      "grants": grants
                  })


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/')
    
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})
