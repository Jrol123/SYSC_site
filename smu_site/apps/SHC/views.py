from django.conf import settings
from django.shortcuts import render
# from documents.models import Doc
from .models import Doc as SHCDoc


def index(request):
    documents = (SHCDoc.objects.select_related('documents.doc')
                 .filter(doc__queue_id__isnull=True)
                 .order_by('documents.doc__id'))
    # print(documents)
    return render(request, 'SHC/index.html',
                  {'docs': documents, 'media': settings.MEDIA_URL})
