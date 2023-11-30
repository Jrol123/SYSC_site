from django.contrib import admin
from .models import (Institute, ScientistInfo, ScientistLink,
                     ScientistPublication, Grant)


admin.site.register(Institute)
admin.site.register(ScientistInfo)
admin.site.register(ScientistLink)
admin.site.register(ScientistPublication)
admin.site.register(Grant)
