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
            "<div class='doc_content_stuff'>"
            f"<a href='{settings.MEDIA_URL}"
            f"{d.path}'>{d.name}</a></div>\n")

    return render(request, 'info/documents.html',
                  {'title': "Документы",
                   'categories': docs_content.items(),
                   "is_moder": request.user.groups.filter(name='moderator').exists(),
                   "is_repr": request.user.groups.filter(name='representative').exists()
                   })
