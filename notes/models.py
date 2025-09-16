# notes/models.py
from django.db import models
from django.utils import timezone

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name

class Note(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(null=False, blank=False, default="")  # já corrigido
    created_at = models.DateTimeField(default=timezone.now, editable=True)  # ← em vez de auto_now_add
    updated_at = models.DateTimeField(auto_now=True)                           # ok manter
    tags = models.ManyToManyField(Tag, related_name="notes", blank=True)

    def __str__(self):
        return self.title
