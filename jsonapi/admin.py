from django.contrib import admin
from django.apps import apps


# auto-register all models
app = apps.get_app_config('jsonapi')
for model_name, model in app.models.items():
    admin.site.register(model)
