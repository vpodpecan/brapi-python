from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField


class RichText(models.Model):
    name = models.CharField(max_length=50)
    content = RichTextUploadingField(blank=True)

    def __str__(self):
        return self.name
