from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField


class HTML_page(models.Model):
    name = models.CharField(max_length=50, unique=True)
    content = RichTextUploadingField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'HTML page'
        verbose_name_plural = 'HTML pages'
