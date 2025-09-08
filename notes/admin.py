from django.contrib import admin
from .models import Note, Tag

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "tag")

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
