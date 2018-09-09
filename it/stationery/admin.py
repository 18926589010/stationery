from django.contrib import admin
from stationery.models import stationery, stat_type,provider,purchase
# Register your models here.

class stationeryadmin(admin.ModelAdmin):
    list_display = ('name','stock_num','stat_type')
    search_fields = ('name', 'stat_type__name')
    fk_fields = ('stat_type__name',)

admin.site.register(stationery,stationeryadmin)