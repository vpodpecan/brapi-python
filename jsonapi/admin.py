from django.contrib import admin
from django.apps import apps
from django.forms import Textarea, ModelForm
from django.db import models as djmodels

from import_export import resources, instance_loaders
from import_export.admin import ImportExportModelAdmin

from jsonapi import models


# # auto-register all models
# app = apps.get_app_config('jsonapi')
# for model_name, model in app.models.items():
#     admin.site.register(model)
#
# # admin.site.register(models.Crop)



class CustomInstanceLoader(instance_loaders.ModelInstanceLoader):
    def get_instance(self, row):
        raise NotImplementedError


# make import-export admin classes for all models on the fly
def makeAdminClass(dbmodel, **kwargs):
    # class FormClass(ModelForm):
    #     def clean_name(self):
    #             return self.cleaned_data["name"]
    #     class Meta:
    #         model = dbmodel
    #         fields = '__all__'

    class ResourceClass(resources.ModelResource):
        # def before_import(self, row, **kwargs):
        #     pass

        # def get_or_init_instance(self, loader, row):
        #     if dbmodel in [models.LocationAdditionalInfo]:
        #         obj = dbmodel.get_or_create(row)
        #         return obj, True
        #     # if 'pkfields' in kwargs:
        #     #     qdata = {f: row[f] for f in kwargs['pkfields']}
        #     #     objs = dbmodel.objects.filter(qdata)
        #     #     if len(objs) > 1:
        #     #         raise KeyError('Invalid data: multiple objects with this value combination exist: {}'.format(str(row)))
        #     #     elif len(objs) == 0:
        #     #         return dbmodel
        #     #
        #     #
        #     #     print('---------------------------------')
        #     #     print(qfields)
        #     else:
        #         # print('aaaaaaaaaaaaaaaaaaaaaaaaaa')
        #         return super(ResourceClass, self).get_or_init_instance(loader, row)

        class Meta:
            model = dbmodel
            skip_unchanged = True
            report_skipped = False
            import_id_fields = kwargs['pkfields']
            #import_id_fields = [dbmodel._meta.pk.column]
            # instance_loader_class = CustomInstanceLoader

    class ModelAdminClass(ImportExportModelAdmin, admin.ModelAdmin):
        resource_class = ResourceClass
        # form = FormClass
        formfield_overrides = {
            djmodels.TextField: {'widget': Textarea(attrs={'rows': 1, 'style': 'resize:vertical;min-height:3em;'})},
        }
    return ModelAdminClass
# end


# auto-register all classes
app = apps.get_app_config('jsonapi')
for model_name, model in app.models.items():
    # # no import-export capabilities for these
    # if model in NOIMPORT_MODELS:
    #     admin.site.register(model)
    #     continue

    # special treatment for tables without explicit primary key
    # this combination of keys is used by import-export to check whether to add or update instance
    if model == models.Donor:
        pks = ['cropDbId', 'germplasmDbId', 'donorGermplasmPUI']
    elif model == models.GermplasmAttributeValue:
        pks = ['cropDbId', 'germplasmDbId', 'attributeDbId']
    elif model == models.LocationAdditionalInfo:
        pks = ['cropDbId', 'locationDbId', 'key']
    elif model == models.Treatment:
        pks = ['cropDbId', 'observationUnitDbId']
    elif model == models.Pedigree:
        pks = ['cropDbId', 'germplasmDbId', 'parent1Id', 'parent2Id']
    elif model == models.StudyAdditionalInfo:
        pks = ['cropDbId', 'studyDbId', 'key']
    elif model == models.StudyDataLink:
        pks = ['cropDbId', 'studyDbId', 'name']
    elif model == models.StudySeason:
        pks = ['cropDbId', 'studyDbId', 'seasonDbId']
    elif model == models.StudyContact:
        pks = ['cropDbId', 'studyDbId', 'contactDbId']
    elif model == models.TaxonXrefGermplasm:
        pks = ['cropDbId', 'taxonDbId', 'germplasmDbId']
    elif model == models.TrialAdditionalInfo:
        pks = ['cropDbId', 'trialDbId', 'key', 'value']
    elif model == models.TrialContact:
        pks = ['cropDbId', 'trialDbId', 'contactDbId']
    else:
        pks = [model._meta.pk.column]

    ac = makeAdminClass(model, pkfields=pks)
    admin.site.register(model, ac)
