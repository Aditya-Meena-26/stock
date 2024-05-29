from django.contrib import admin
from .models import StockData, Prediction
# Register your models here.
admin.site.register(StockData)
admin.site.register(Prediction)