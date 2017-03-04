from django.contrib import admin

from contests.models import Contest, ContestManager, MCQuestion, WritingQuestion, Match


# Register your models here.
admin.site.register(Contest)
admin.site.register(ContestManager)
admin.site.register(MCQuestion)
admin.site.register(WritingQuestion)
admin.site.register(Match)
