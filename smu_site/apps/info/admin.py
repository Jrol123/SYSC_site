from django.contrib import admin

from .models import Institute, Scientist, ScientistLink, Grant


admin.site.register(Institute)
admin.site.register(Scientist)
admin.site.register(ScientistLink)
admin.site.register(Grant)
