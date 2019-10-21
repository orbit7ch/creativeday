from django.contrib import admin

from core.export_action import export_as_excel
from core.models import GenericEvent


@admin.register(GenericEvent)
class GenericEventAdmin(admin.ModelAdmin):
    list_display = ['created', 'title', 'fields_clean', 'reported', 'is_internal']
    search_fields = ['title', 'fields', 'fields', 'ga_id']
    list_filter = ['title', 'reported', 'is_internal']
    actions = [export_as_excel]
    export_flatten_fields = ['fields']