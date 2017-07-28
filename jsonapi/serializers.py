from rest_framework import serializers

from jsonapi import models


class GermplasmDetailsSerializer(serializers.ModelSerializer):
    commonCropName = serializers.SlugRelatedField(many=False, read_only=True, slug_field='commonName', source='cropDbId')

    class Meta:
        model = models.Germplasm
        # fields = '__all__'
        exclude = ('cropDbId',)
