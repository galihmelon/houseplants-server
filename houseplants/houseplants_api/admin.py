from django.contrib import admin
from houseplants_api.models import Plant, CleaningLog, WateringLog

admin.site.register(Plant)
admin.site.register(CleaningLog)
admin.site.register(WateringLog)
