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


def index(request):
    # Получаем даты для фильтрации списка новостей
    # sdate = datetime.combine(date.fromisoformat(
    #     request.POST.get("start-date", "2023-11-28")),
    #     datetime.min.time()).isoformat()
    # edate = datetime.combine(date.fromisoformat(
    #     request.POST.get("end-date", localdate().isoformat())),
    #     datetime.min.time())
    sdate = date.fromisoformat(
            request.POST.get("start-date", "2023-11-28"))
    edate = date.fromisoformat(
            request.POST.get("end-date", localdate().isoformat()))
    
    edate += timedelta(days=1)
    
    # Выбираем те новости и события, которые не находятся в очереди
    latest_news = list(News.objects.filter(pub_date__range=(sdate, edate)))
    latest_events = list(Event.objects.filter(pub_date__range=(sdate, edate)))
    latest_news += latest_events
    print(repr(latest_news))
    
    # Сортируем по дате и выбираем первые 5 для первой страницы новостей
    latest_news = list(sorted(latest_news, key=lambda x: x.pub_date,
                              reverse=True))
    if len(latest_news) > 5:
        latest_news = latest_news[:5]
    
    # объединяем со списков месяцев
    month = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
             'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    latest_news = [(n, month[n.pub_date.month - 1])
                   for n in latest_news]
    
    sdate = sdate.isoformat()
    edate -= timedelta(days=1)
    edate = edate.isoformat()
    return render(request, 'index.html',
                  {
                      "latest_news_month": latest_news,
                      "sdate": sdate, "edate": edate})


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
