from rest_framework import serializers

from jsonapi import models


class GermplasmDetailsSerializer(serializers.ModelSerializer):
    commonCropName = serializers.SlugRelatedField(many=False, read_only=True, slug_field='commonName', source='cropDbId')

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


class StudyTrialSerializer(serializers.ModelSerializer):
    locationName = serializers.SlugRelatedField(many=False, read_only=True, slug_field='locationName', source='locationDbId')

    class Meta:
        model = models.Study
        safe = False
        fields = ('studyDbId', 'studyName', 'locationDbId', 'locationName')


class TrialDetailsSerializer(serializers.ModelSerializer):
    studies = StudyTrialSerializer(source='study_set', many=True)
    # active = serializers.CharField()

    class Meta:
        model = models.Trial
        safe = False
        fields = '__all__'
        # fields = ('studies',)



# class DatasetAuthorshipSerializerserializers.Serializer):
#     license = serializers.EmailField()
#     datasetPUI = serializers.CharField(max_length=100)


# class TrialDetailsSerializer(serializers.ModelSerializer):
#     studies = StudyTrialSerializer(source='study_set')
#
#     class Meta:
#         model = models.Trial
#         safe = False
#         exclude = ('datasetAuthorshipLicence', 'datasetAuthorshipDatasetPUI')
    #
    # cropDbId = models.ForeignKey('Crop', verbose_name=' cropDbId')
    # programDbId = models.ForeignKey('Program', verbose_name=' programDbId')
    # trialDbId = models.TextField(primary_key=True, verbose_name=' trialDbId')
    # trialName = models.TextField(verbose_name=' name')
    # startDate = models.TextField(blank=True, verbose_name=' startDate')
    # endDate = models.TextField(blank=True, verbose_name=' endDate')
    # active = models.NullBooleanField(verbose_name=' active')
    # datasetAuthorshipLicence = models.TextField(blank=True, verbose_name=' datasetAuthorshipLicence')
    # datasetAuthorshipDatasetPUI = models.TextField(blank=True, verbose_name=' datasetAuthorshipDatasetPUI')
    #


        # "trialDbId" : 1,
        # "trialName" : "InternationalTrialA",
        # "programDbId": 27,
        # "programName": "International Yield Trial",
        # "startDate": "2007-06-01",
        # "endDate"  : "2008-12-31",
        # "active" : "true",
        # "datasetAuthorship":{
        #     "license": "https://creativecommons.org/licenses/by/4.0",
        #     "datasetPUI":"doi:10.15454/312953986E3"
        #
