from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from django.utils.timezone import localdate
from datetime import date, timedelta
from news.models import News, Event


def index(request):
    # Получаем даты для фильтрации списка новостей
    sdate = date.fromisoformat(
        request.POST.get("start-date", "2023-11-28"))
    edate = request.POST.get("end-date", localdate())
    if not isinstance(edate, date):
        edate = date.fromisoformat(edate)
    
    edate += timedelta(days=2)
    
    # Выбираем те новости и события, которые не находятся в очереди
    latest_news = list(filter(lambda x: not x.queue_id,
                              News.objects.filter(
                                  pub_date__range=(sdate, edate))))
    latest_events = list(filter(lambda x: not x.queue_id,
                                Event.objects.filter(
                                    pub_date__range=(sdate, edate))))
    latest_news += latest_events
    
    # Сортируем по дате и выбираем первые 5 для первой страницы новостей
    latest_news = list(sorted(latest_news, key=lambda x: x.pub_date))
    if len(latest_news) > 5:
        latest_news = latest_news[:5]
    
    # объединяем со списков месяцев
    month = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
             'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    latest_news = [(n, month[n.pub_date.month - 1])
                   for n in latest_news]
    
    edate -= timedelta(days=2)
    sdate = sdate.isoformat()
    edate = edate.isoformat()
    return render(request, 'index.html',
                  {
                      "latest_news_month": latest_news,
                      "sdate": sdate, "edate": edate})
