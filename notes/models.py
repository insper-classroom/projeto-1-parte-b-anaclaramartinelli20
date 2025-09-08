from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

class Note(models.Model):
    title = models.CharField(max_length=200, default="")
    content = models.TextField(null=True, default="")
    tag = models.ForeignKey(Tag, null=True, blank=True, on_delete=models.SET_NULL)

