from django.shortcuts import render
from django.conf import settings
from .models import Category, Doc


def index(request):
    # kitkat = Category.objects.all().order_by('name')
    docs = (Doc.objects.select_related('category')
            .filter(queue_id__isnull=True,
                    category__isnull=False).order_by('category__name',
                                                     'name'))
    docs_content = {}
    for d in docs:
        if not docs_content.get(d.category.name):
            docs_content[d.category.name] = ""
        
        docs_content[d.category.name] += (
            f"<a href='{settings.MEDIA_URL}"
            f"{d.path}'><h1>{d.name}</h1></a>\n")
        
    return render(request, 'info/documents.html',
                  {'title': "Документы",
                   'categories': docs_content.items()})
