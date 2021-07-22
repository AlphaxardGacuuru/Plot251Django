from django.contrib import admin

# Register your models here.
from .models import WaterReadings, WaterPayments

admin.site.site_header = "Plot251 Admin"
admin.site.site_title = "Plot251 Admin Area"
admin.site.index_title = "Welcome to the Plot251 Admin Area"

admin.site.register(WaterReadings)
admin.site.register(WaterPayments)
