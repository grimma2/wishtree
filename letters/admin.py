from django.contrib import admin
from .models import Letter, Child, Gift
from django.contrib.auth.models import Permission


@admin.register(Letter)
class LetterAdmin(admin.ModelAdmin):
    list_display = ('photo', 'child', 'gift', 'picked_by', 'id')
    list_display_links = ('id', 'gift', 'child')


@admin.register(Child)
class ChildAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'id')
    list_display_links = ('id',)


@admin.register(Gift)
class ChildAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'id')
    list_display_links = ('name', 'id')


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ('codename', 'name', 'content_type')
