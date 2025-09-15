# notes/admin.py
from django.contrib import admin
from .models import Note, Tag

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'tag_list')
    search_fields = ('title', 'content', 'tags__name')
    filter_horizontal = ('tags',)  # widget bacana de seleção M2M

    def tag_list(self, obj):
        return ", ".join(obj.tags.values_list('name', flat=True))

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ('name',)
