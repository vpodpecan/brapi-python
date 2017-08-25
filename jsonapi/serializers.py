from rest_framework import serializers

from jsonapi import models
from jsonapi import utils


class Germplasm_DonorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Donor
        safe = False
        exclude = ('cropDbId', 'germplasmDbId', 'id')


class GermplasmDetailsSerializer(serializers.ModelSerializer):
    commonCropName = serializers.SlugRelatedField(many=False, read_only=True, slug_field='commonName', source='cropDbId')
    donors = Germplasm_DonorSerializer(many=True, source='donor_set')
    # taxonIds = Germplasm_TaxonXrefGermplasmSerializer(many=True, source='taxonxrefgermplasm_set')
    taxonIds = serializers.SerializerMethodField()
    synonyms = serializers.SerializerMethodField()

    def get_taxonIds(self, obj):
        data = []
        for txr in obj.taxonxrefgermplasm_set.all():
            data.append({txr.taxonDbId.source: txr.taxonDbId.taxonDbId})
        return data

    def get_synonyms(self, obj):
        return utils.valueArrayFromString(obj.synonyms)

    class Meta:
        model = models.Germplasm
        safe = False
        # fields = '__all__'
        exclude = ('cropDbId',)


class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Program
        safe = False
        exclude = ('cropDbId',)


class Trial_TrialAdditionalInfoSerializer(serializers.ModelSerializer):
    additionalInfo = serializers.SerializerMethodField()

    def get_additionalInfo(self, obj):
        data = {}
        data[obj.key] = obj.value
        return data

    class Meta:
        model = models.TrialAdditionalInfo
        fields = ('additionalInfo',)
        # fields = '__all__'


class Trial_StudySerializer(serializers.ModelSerializer):
    locationName = serializers.SlugRelatedField(many=False, read_only=True, slug_field='name', source='locationDbId')
    studyName = serializers.SerializerMethodField()

    def get_studyName(self, obj):
        return obj.name

    class Meta:
        model = models.Study
        safe = False
        fields = ('studyDbId', 'studyName', 'locationDbId', 'locationName')


class Trial_TrialContactSerializer(serializers.ModelSerializer):
    name = serializers.SlugRelatedField(many=False, read_only=True, slug_field='name', source='contactDbId')
    instituteName = serializers.SlugRelatedField(many=False, read_only=True, slug_field='instituteName', source='contactDbId')
    email = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email', source='contactDbId')
    type = serializers.SlugRelatedField(many=False, read_only=True, slug_field='type', source='contactDbId')
    orcid = serializers.SlugRelatedField(many=False, read_only=True, slug_field='orcid', source='contactDbId')

    class Meta:
        model = models.Contact
        safe = False
        fields = ('contactDbId', 'name', 'instituteName', 'email', 'type', 'orcid')


class TrialSummarySerializer(serializers.ModelSerializer):
    studies = Trial_StudySerializer(source='study_set', many=True)
    programName = serializers.SlugRelatedField(many=False, read_only=True, slug_field='name', source='programDbId')
    active = serializers.SerializerMethodField()
    additionalInfo = serializers.SerializerMethodField()
    trialName = serializers.SerializerMethodField()

    def get_trialName(self, obj):
        return obj.name

    def get_active(self, obj):
        return str(obj.active).lower()

    def get_additionalInfo(self, obj):
        # documentation is unclear about this, so we will not create empty arrays for publications beforehand
        # i.e. 'publications' key will only appear if there is nonempty list of publications
        data = {}
        for x in obj.trialadditionalinfo_set.all():
            if x.key not in data:
                data[x.key] = x.value
            else:
                # append or transform into a list and append
                if isinstance(data[x.key], list):
                    data[x.key].append(x.value)
                else:
                    data[x.key] = [data[x.key], x.value]
        return data

    class Meta:
        model = models.Trial
        safe = False
        # fields = '__all__'
        # fields = ('trialDbId', 'trialName', 'programDbId', 'programName', 'startDate',
        #           'endDate', 'active', 'studies', 'contacts', 'datasetAuthorship')
        exclude = ('cropDbId', 'datasetAuthorshipLicence', 'datasetAuthorshipDatasetPUI', 'name')  # we have to rename 'name' to 'trialName'...


class TrialDetailsSerializer(TrialSummarySerializer):
    contacts = Trial_TrialContactSerializer(source='trialcontact_set', many=True)
    datasetAuthorship = serializers.SerializerMethodField()

    def get_datasetAuthorship(self, obj):
        datasetAuthorship_fields = {}
        datasetAuthorship_fields['datasetAuthorshipLicence'] = obj.datasetAuthorshipLicence
        datasetAuthorship_fields['datasetAuthorshipDatasetPUI'] = obj.datasetAuthorshipDatasetPUI
        return datasetAuthorship_fields
