from django.contrib import admin
from .models import Institute, ScientistInfo, Grant


admin.site.register(Institute)
admin.site.register(ScientistInfo)
admin.site.register(Grant)
