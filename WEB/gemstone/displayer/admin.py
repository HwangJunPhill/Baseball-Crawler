from django.contrib import admin
from .models import DailyRecord, Profile, SeasonRecord, TotalRecord

# Register your models here.

admin.site.register(DailyRecord)
admin.site.register(Profile)
admin.site.register(SeasonRecord)
admin.site.register(TotalRecord)