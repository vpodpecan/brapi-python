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


class Trial_StudySerializer(serializers.ModelSerializer):
    locationName = serializers.SlugRelatedField(many=False, read_only=True, slug_field='name', source='locationDbId')
    studyName = serializers.CharField(source='name')

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
    trialName = serializers.CharField(source='name')

    def get_active(self, obj):
        return bool2text(obj.active)

    def get_additionalInfo(self, obj):
        return collect_additional_info(obj.trialadditionalinfo_set.all())

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


class LocationSerializer(serializers.ModelSerializer):
    additionalInfo = serializers.SerializerMethodField()

    def get_additionalInfo(self, obj):
        return collect_additional_info(obj.locationadditionalinfo_set.all())

    class Meta:
        model = models.Location
        safe = False
        exclude = ['cropDbId', 'type']


class StudyDetailsSerializer(serializers.ModelSerializer):
    contacts = Trial_TrialContactSerializer(source='studycontact_set', many=True)  # can be reused from Trial
    location = LocationSerializer(source='locationDbId', many=False)
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
    trialName = serializers.SlugRelatedField(many=False, read_only=True, slug_field='name', source='trialDbId')
    # studyType = serializers.SlugRelatedField(many=False, read_only=True, slug_field='name')
    seasons = serializers.SerializerMethodField()
    locationName = serializers.SlugRelatedField(many=False, read_only=True, slug_field='name', source='locationDbId')
    programDbId = serializers.SerializerMethodField()
    programName = serializers.SerializerMethodField()
    additionalInfo = serializers.SerializerMethodField()
    active = serializers.SerializerMethodField()

    def get_seasons(self, obj):
        seasons = []
        for studyseason in obj.studyseason_set.all():
            seasons.append(studyseason.seasonDbId.season)
        return seasons

    def get_active(self, obj):
        return bool2text(obj.active)

    def get_programDbId(self, obj):
        return obj.trialDbId.programDbId.programDbId

    def get_programName(self, obj):
        return obj.trialDbId.programDbId.name

    def get_additionalInfo(self, obj):
        return collect_additional_info(obj.studyadditionalinfo_set.all())

    class Meta:
        model = models.Study
        safe = False
        exclude = ['lastUpdateVersion', 'lastUpdateTimestamp', 'description']
