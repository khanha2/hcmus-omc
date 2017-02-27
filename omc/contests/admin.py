from django.contrib import admin

from contests.models import Contest, ContestManager

# Register your models here.
admin.site.register(Contest)
admin.site.register(ContestManager)
