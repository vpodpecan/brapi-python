from rest_framework import serializers

from jsonapi import models
from jsonapi import utils


def collect_additional_info(objectset):
    data = {}
    for x in objectset:
        if x.key not in data:
            data[x.key] = x.value
        else:
            # append or transform into a list and append
            if isinstance(data[x.key], list):
                data[x.key].append(x.value)
            else:
                data[x.key] = [data[x.key], x.value]
    return data


def bool2text(x):
    return str(x).lower()


class Germplasm_DonorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Donor
        safe = False
        exclude = ('cropDbId', 'germplasmDbId', 'id')


class GermplasmDetailsSerializer(serializers.ModelSerializer):
    commonCropName = serializers.CharField(source='cropDbId.commonName')
    donors = Germplasm_DonorSerializer(many=True, source='donor_set')
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


class Trial_StudySerializer(serializers.ModelSerializer):
    locationName = serializers.CharField(source='locationDbId.name')
    studyName = serializers.CharField(source='name')

    class Meta:
        model = models.Study
        safe = False
        fields = ('studyDbId', 'studyName', 'locationDbId', 'locationName')


class Trial_TrialContactSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='contactDbId.name')
    instituteName = serializers.CharField(source='contactDbId.instituteName')
    email = serializers.CharField(source='contactDbId.email')
    type = serializers.CharField(source='contactDbId.type')
    orcid = serializers.CharField(source='contactDbId.orcid')

    class Meta:
        model = models.Contact
        safe = False
        fields = ('contactDbId', 'name', 'instituteName', 'email', 'type', 'orcid')


class TrialSummarySerializer(serializers.ModelSerializer):
    studies = Trial_StudySerializer(source='study_set', many=True)
    programName = serializers.CharField(source='programDbId.name')
    active = serializers.SerializerMethodField()
    additionalInfo = serializers.SerializerMethodField()
    trialName = serializers.CharField(source='name')

    def get_active(self, obj):
        return bool2text(obj.active)

    def get_additionalInfo(self, obj):
        return collect_additional_info(obj.trialadditionalinfo_set.all())

    class Meta:
        model = models.Trial
        safe = False
        # fields = '__all__'
        exclude = ('cropDbId', 'datasetAuthorshipLicence', 'datasetAuthorshipDatasetPUI', 'name')


class TrialDetailsSerializer(TrialSummarySerializer):
    contacts = Trial_TrialContactSerializer(source='trialcontact_set', many=True)
    datasetAuthorship = serializers.SerializerMethodField()

    def get_datasetAuthorship(self, obj):
        datasetAuthorship_fields = {}
        datasetAuthorship_fields['datasetAuthorshipLicence'] = obj.datasetAuthorshipLicence
        datasetAuthorship_fields['datasetAuthorshipDatasetPUI'] = obj.datasetAuthorshipDatasetPUI
        return datasetAuthorship_fields


class StudyDetails_LocationSerializer(serializers.ModelSerializer):
    additionalInfo = serializers.SerializerMethodField()

    def get_additionalInfo(self, obj):
        return collect_additional_info(obj.locationadditionalinfo_set.all())

    class Meta:
        model = models.Location
        safe = False
        exclude = ['cropDbId', 'type']


class StudyDetailsSerializer(serializers.ModelSerializer):
    contacts = Trial_TrialContactSerializer(source='studycontact_set', many=True)  # can be reused from Trial
    location = StudyDetails_LocationSerializer(source='locationDbId', many=False)
    studyDescription = serializers.CharField(source='description')
    additionalInfo = serializers.SerializerMethodField()
    lastUpdate = serializers.SerializerMethodField()
    seasons = serializers.SerializerMethodField()
    active = serializers.SerializerMethodField()

    def get_seasons(self, obj):
        seasons = []
        for studyseason in obj.studyseason_set.all():
            seasons.append(studyseason.seasonDbId.season)
        return seasons

    def get_active(self, obj):
        return bool2text(obj.active)

    def get_lastUpdate(self, obj):
        lastUpdate_fields = {}
        lastUpdate_fields['version'] = obj.lastUpdateVersion
        lastUpdate_fields['timestamp'] = obj.lastUpdateTimestamp
        return lastUpdate_fields

    def get_additionalInfo(self, obj):
        return collect_additional_info(obj.studyadditionalinfo_set.all())

    class Meta:
        model = models.Study
        safe = False
        exclude = ['lastUpdateVersion', 'lastUpdateTimestamp']


class StudySummarySerializer(serializers.ModelSerializer):
    trialName = serializers.CharField(source='trialDbId.name')
    seasons = serializers.SerializerMethodField()
    locationName = serializers.CharField(source='locationDbId.name')
    programDbId = serializers.CharField(source='trialDbId.programDbId.programDbId')
    programName = serializers.CharField(source='trialDbId.programDbId.name')
    additionalInfo = serializers.SerializerMethodField()
    active = serializers.SerializerMethodField()

    def get_seasons(self, obj):
        seasons = []
        for studyseason in obj.studyseason_set.all():
            seasons.append(studyseason.seasonDbId.season)
        return seasons

    def get_active(self, obj):
        return bool2text(obj.active)

    def get_additionalInfo(self, obj):
        return collect_additional_info(obj.studyadditionalinfo_set.all())

    class Meta:
        model = models.Study
        safe = False
        exclude = ['lastUpdateVersion', 'lastUpdateTimestamp', 'description']


class ObservationVariable_TraitSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Trait
        safe = False
        exclude = ['cropDbId']


class ObservationVariable_MethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Method
        safe = False
        exclude = ['cropDbId']


class ObservationVariable_ScaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Scale
        safe = False
        exclude = ['cropDbId']


class ObservationVariableSerializer(serializers.ModelSerializer):
    trait = ObservationVariable_TraitSerializer(source='traitDbId')
    method = ObservationVariable_MethodSerializer(source='methodDbId')
    scale = ObservationVariable_ScaleSerializer(source='scaleDbId')
    name = serializers.CharField(source='observationVariableName')
    ontologyName = serializers.CharField(source='ontologyDbId.name')
    synonyms = serializers.SerializerMethodField()
    contextOfUse = serializers.SerializerMethodField()

    def get_synonyms(self, obj):
        return []  # not yet specified by BRAPI

    def get_contextOfUse(self, obj):
        return []  # not yet specified by BRAPI

    class Meta:
        model = models.ObservationVariable
        safe = False
        exclude = ['traitDbId']


class Study_GermplasmSerializer(serializers.ModelSerializer):
    # commonCropName = serializers.CharField(source='cropDbId.commonName')
    # donors = Germplasm_DonorSerializer(many=True, source='donor_set')
    # taxonIds = serializers.SerializerMethodField()
    synonyms = serializers.SerializerMethodField()

    # def get_taxonIds(self, obj):
    #     data = []
    #     for txr in obj.taxonxrefgermplasm_set.all():
    #         data.append({txr.taxonDbId.source: txr.taxonDbId.taxonDbId})
    #     return data

    def get_synonyms(self, obj):
        return utils.valueArrayFromString(obj.synonyms)

    class Meta:
        model = models.Germplasm
        safe = False
        # some of the fields are not yet defined by BRAPI!
        # fields = ['germplasmDbId', "entryNumber", "germplasmName", "pedigree", "seedSource", "accessionNumber",
        #           "germplasmPUI", "synonyms"]
        fields = ['germplasmDbId', "germplasmName", "pedigree", "seedSource", "accessionNumber",
                  "germplasmPUI", "synonyms"]


class LocationSerializer(serializers.ModelSerializer):
    locationType = serializers.CharField(source='type')
    additionalInfo = serializers.SerializerMethodField()

    def get_additionalInfo(self, obj):
        return collect_additional_info(obj.locationadditionalinfo_set.all())

    class Meta:
        model = models.Location
        safe = False
        # fields = []
        exclude = ['cropDbId']
