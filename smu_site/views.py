from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from news.models import News, Event


def index(request):
    latest_news = list(News.objects.all())
    latest_events = list(Event.objects.all())
    latest_news += latest_events
    latest_news = list(sorted(latest_news, key=lambda x: x.pub_date))
    if len(latest_news) > 5:
        latest_news = latest_news[:5]
        
    month = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
             'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    latest_news = [(n, month[n.pub_date.month - 1]) for n in latest_news]
    
    print(latest_news)
    
    return render(request, 'index.html',
                  {"latest_news_month": latest_news})
