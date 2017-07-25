from django.contrib import admin
from django.apps import apps
from django.forms import Textarea, ModelForm
from django.db import models as djmodels

from import_export import resources
from import_export.admin import ImportExportModelAdmin

# from jsonapi import models


# # auto-register all models
# app = apps.get_app_config('jsonapi')
# for model_name, model in app.models.items():
#     admin.site.register(model)
#
# # admin.site.register(models.Crop)


# make import-export admin classes for all models on the fly
def makeAdminClass(dbmodel):
    # class FormClass(ModelForm):
    #     def clean_name(self):
    #             return self.cleaned_data["name"]
    #     class Meta:
    #         model = dbmodel
    #         fields = '__all__'

    class ResourceClass(resources.ModelResource):
        class Meta:
            model = dbmodel
            import_id_fields = [dbmodel._meta.pk.column]

    class ModelAdminClass(ImportExportModelAdmin, admin.ModelAdmin):
        resource_class = ResourceClass
        # form = FormClass
        formfield_overrides = {
            djmodels.TextField: {'widget': Textarea(attrs={'rows': 1, 'style': 'resize:vertical;min-height:3em;'})},
        }
    return ModelAdminClass
# end


# auto-register all created admin classes
app = apps.get_app_config('jsonapi')
for model_name, model in app.models.items():
    ac = makeAdminClass(model)
    admin.site.register(model, ac)
