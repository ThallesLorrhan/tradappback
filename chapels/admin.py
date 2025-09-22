from django.contrib import admin
from .models import Chapel

@admin.register(Chapel)
class ChapelAdmin(admin.ModelAdmin):
    list_display = ('name', 'subtitle', 'priest', 'miss_type', 'phone_number', 'day_of_week', 'schedule')
    search_fields = ('name', 'priest', 'address')
    list_filter = ('miss_type', 'day_of_week')
