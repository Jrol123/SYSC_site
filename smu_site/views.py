import os
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader
from django.shortcuts import render
from django.utils.timezone import localdate
from datetime import date, timedelta, datetime
from news.models import News, Event
from .forms import LoginForm
from django.contrib.auth import authenticate, login
from django.core.exceptions import ValidationError
from info.models import Grant


def index(request):
    # Получаем даты для фильтрации списка новостей
    sdate = date.fromisoformat(
            request.POST.get("start-date", "2023-11-28"))
    edate = date.fromisoformat(
            request.POST.get("end-date", localdate().isoformat()))
    edate += timedelta(days=1)
    
    # Выбираем те новости и события, которые не находятся в очереди
    last_news = list(News.objects.filter(
        pub_date__range=(sdate, edate), queue_id__isnull=True))
    last_events = list(Event.objects.filter(
        pub_date__range=(sdate, edate), queue_id__isnull=True))
    last_news += last_events
    
    # Сортируем по дате и выбираем первые 5 для первой страницы новостей
    last_news = list(sorted(last_news, key=lambda x: x.pub_date,
                            reverse=True))
    if len(last_news) > 5:
        last_news = last_news[:5]
    
    # объединяем со списков месяцев
    month = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
             'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    last_news = [(n, month[n.pub_date.month - 1])
                   for n in last_news]
    
    # переводим даты в изначальный формат
    sdate = sdate.isoformat()
    edate -= timedelta(days=1)
    edate = edate.isoformat()
    
    # Получаем актуальные события и гранты
    events = (Event.objects.filter(queue_id__isnull=True)
              .order_by('begin_date', '-pub_date'))[:3]
    grants = (Grant.objects.filter(queue_id__isnull=True)
              .order_by('end_doc_date'))[:3]
    
    return render(request, 'index.html',
                  {
                      "last_news_month": last_news,
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
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/')

    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})
