from django.shortcuts import render
from django.conf import settings
from .models import Category, Doc


def index(request):
    docs = (Doc.objects.select_related('category')
            .filter(queue_id__isnull=True,
                    category__isnull=False).order_by('category__name',
                                                     'name'))
    docs_content = {}
    for d in docs:
        if not docs_content.get(d.category.name):
            docs_content[d.category.name] = ["", 0]

        docs_content[d.category.name][0] += (
            "<div class='doc_content_stuff'>"
            f"<a href='{settings.MEDIA_URL}"
            f"{d.path}'>{d.name}</a></div>\n")
        docs_content[d.category.name][1] = d.id

    return render(request, 'info/documents.html',
                  {'title': "Документы",
                   'categories': [(c, *docs_content[c]) for c in docs_content],
                   "is_moder": request.user.groups.filter(name='moderator').exists(),
                   "is_repr": request.user.groups.filter(name='representative').exists()
                   })
