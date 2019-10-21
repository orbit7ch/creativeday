from django.contrib import admin
from taggit.models import Tag

from .models import CmsImage, CmsRendition, UserSearchTerm
from core.export_action import export_as_excel


@admin.register(CmsImage)
class CmsImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'rating']
    search_fields = ['title']


@admin.register(CmsRendition)
class CmsRenditionAdmin(admin.ModelAdmin):
    pass


@admin.register(UserSearchTerm)
class UserSearchTermAdmin(admin.ModelAdmin):
    list_display = ['created', 'fields_clean', 'is_internal', 'nbr_results', 'has_results', 'reported']
    search_fields = ['session_id', 'fields', 'ga_id']
    list_filter = ['is_internal', 'has_results']
    actions = [export_as_excel]
    export_flatten_fields = ['fields']


admin.site.unregister(Tag)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name', 'slug']
    actions = [export_as_excel]
    export_fields_only = ['id', 'name', 'slug']
