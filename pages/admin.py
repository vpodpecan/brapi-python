from django.contrib import admin

from pages import models


class HTML_page_admin(admin.ModelAdmin):
    fields = ('name', 'content')
    # readonly_fields = ('name',)


admin.site.register(models.HTML_page, HTML_page_admin)
