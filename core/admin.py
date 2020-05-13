from django.contrib import admin

from .models import CTeam, CSpace, CFolder, CList, CTask

admin.site.register(CTeam)
admin.site.register(CSpace)
admin.site.register(CFolder)
admin.site.register(CList)
admin.site.register(CTask)
