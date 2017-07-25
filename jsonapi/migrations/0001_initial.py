# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-25 14:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('contactDbId', models.TextField(primary_key=True, serialize=False, verbose_name='contactDbId')),
                ('name', models.TextField(blank=True, verbose_name='name')),
                ('email', models.TextField(blank=True, verbose_name='email')),
                ('type', models.TextField(blank=True, verbose_name='type')),
                ('orcid', models.TextField(blank=True, verbose_name='orcid')),
                ('instituteName', models.TextField(blank=True, verbose_name='instituteName')),
            ],
        ),
        migrations.CreateModel(
            name='Crop',
            fields=[
                ('cropDbId', models.TextField(primary_key=True, serialize=False, verbose_name='cropDbId')),
                ('commonName', models.TextField(verbose_name='commonName')),
            ],
        ),
        migrations.CreateModel(
            name='Donor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('donorAccessionNumber', models.TextField(blank=True, verbose_name='donorAccessionNumber')),
                ('donorInstituteCode', models.TextField(blank=True, verbose_name='donorInstituteCode')),
                ('donorGermplasmPUI', models.TextField(blank=True, verbose_name='donorGermplasmPUI')),
                ('cropDbId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jsonapi.Crop', verbose_name='cropDbId')),
            ],
        ),
        migrations.CreateModel(
            name='Germplasm',
            fields=[
                ('germplasmDbId', models.TextField(primary_key=True, serialize=False, verbose_name='germplasmDbId')),
                ('germplasmPUI', models.TextField(blank=True, verbose_name='germplasmPUI')),
                ('germplasmName', models.TextField(verbose_name='germplasmName')),
                ('defaultDisplayName', models.TextField(verbose_name='defaultDisplayName')),
                ('accessionNumber', models.TextField(blank=True, verbose_name='accessionNumber')),
                ('pedigree', models.TextField(blank=True, verbose_name='pedigree')),
                ('seedSource', models.TextField(blank=True, verbose_name='seedSource')),
                ('synonyms', models.TextField(blank=True, verbose_name='synonyms')),
                ('instituteCode', models.TextField(verbose_name='instituteCode')),
                ('instituteName', models.TextField(blank=True, verbose_name='instituteName')),
                ('biologicalStatusOfAccessionCode', models.TextField(blank=True, verbose_name='biologicalStatusOfAccessionCode')),
                ('countryOfOriginCode', models.TextField(blank=True, verbose_name='countryOfOriginCode')),
                ('typeOfGermplasmStorageCode', models.TextField(blank=True, verbose_name='typeOfGermplasmStorageCode')),
                ('genus', models.TextField(blank=True, verbose_name='genus')),
                ('species', models.TextField(blank=True, verbose_name='species')),
                ('speciesAuthority', models.TextField(blank=True, verbose_name='speciesAuthority')),
                ('subtaxa', models.TextField(blank=True, verbose_name='subtaxa')),
                ('subtaxaAuthority', models.TextField(blank=True, verbose_name='subtaxaAuthority')),
                ('acquisitionDate', models.TextField(blank=True, verbose_name='acquisitionDate')),
                ('cropDbId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jsonapi.Crop', verbose_name='cropDbId')),
            ],
        ),
        migrations.CreateModel(
            name='GermplasmAttribute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attributeDbId', models.TextField(unique=True, verbose_name='attributeDbId')),
                ('code', models.TextField(blank=True, verbose_name='code')),
                ('uri', models.TextField(blank=True, verbose_name='uri')),
                ('name', models.TextField(verbose_name='name')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('datatype', models.TextField(blank=True, verbose_name='datatype')),
                ('values', models.TextField(blank=True, verbose_name='values')),
            ],
        ),
        migrations.CreateModel(
            name='GermplasmAttributeCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attributeCategoryDbId', models.TextField(unique=True, verbose_name='attributeCategoryDbId')),
                ('attributeCategoryName', models.TextField(blank=True, verbose_name='attributeCategoryName')),
                ('cropDbId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jsonapi.Crop', verbose_name='cropDbId')),
            ],
        ),
        migrations.CreateModel(
            name='GermplasmAttributeValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('determinedDate', models.TextField(blank=True, verbose_name='determinedDate')),
                ('value', models.TextField(verbose_name='value')),
                ('attributeDbId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jsonapi.GermplasmAttribute', verbose_name='attributeDbId')),
                ('cropDbId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jsonapi.Crop', verbose_name='cropDbId')),
                ('germplasmDbId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jsonapi.Germplasm', verbose_name='germplasmDbId')),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('locationDbId', models.TextField(primary_key=True, serialize=False, verbose_name='locationDbId')),
                ('type', models.TextField(blank=True, verbose_name='type')),
                ('name', models.TextField(blank=True, verbose_name='name')),
                ('abbreviation', models.TextField(blank=True, verbose_name='abbreviation')),
                ('countryCode', models.TextField(blank=True, verbose_name='countryCode')),
                ('countryName', models.TextField(blank=True, verbose_name='countryName')),
                ('latitude', models.TextField(blank=True, verbose_name='latitude')),
                ('longitude', models.TextField(blank=True, verbose_name='longitude')),
                ('altitude', models.TextField(blank=True, verbose_name='altitude')),
                ('instituteName', models.TextField(blank=True, verbose_name='instituteName')),
                ('instituteAddress', models.TextField(blank=True, verbose_name='instituteAddress')),
                ('cropDbId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jsonapi.Crop', verbose_name='cropDbId')),
            ],
        ),
        migrations.CreateModel(
            name='LocationAdditionalInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.TextField(verbose_name='key')),
                ('value', models.TextField(verbose_name='value')),
                ('cropDbId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jsonapi.Crop', verbose_name='cropDbId')),
                ('locationDbId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jsonapi.Location', verbose_name='locationDbId')),
            ],
        ),
        migrations.CreateModel(
            name='Map',
            fields=[
                ('mapDbId', models.TextField(primary_key=True, serialize=False, verbose_name='mapDbId')),
                ('cropDbId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jsonapi.Crop', verbose_name='cropDbId')),
            ],
        ),
        migrations.CreateModel(
            name='Marker',
            fields=[
                ('markerDbId', models.TextField(primary_key=True, serialize=False, verbose_name='markerDbId')),
                ('defaultDisplayName', models.TextField(blank=True, verbose_name='defaultDisplayName')),
                ('type', models.TextField(blank=True, verbose_name='type')),
                ('synonyms', models.TextField(blank=True, verbose_name='synonyms')),
                ('refAlt', models.TextField(blank=True, verbose_name='refAlt')),
                ('analysisMethods', models.TextField(blank=True, verbose_name='analysisMethods')),
                ('cropDbId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jsonapi.Crop', verbose_name='cropDbId')),
            ],
        ),
        migrations.CreateModel(
            name='Markerprofile',
            fields=[
                ('markerProfileDbId', models.TextField(primary_key=True, serialize=False, verbose_name='markerProfileDbId')),
                ('cropDbId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jsonapi.Crop', verbose_name='cropDbId')),
            ],
        ),
        migrations.CreateModel(
            name='Method',
            fields=[
                ('methodDbId', models.TextField(primary_key=True, serialize=False, verbose_name='methodDbId')),
                ('cropDbId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jsonapi.Crop', verbose_name='cropDbId')),
            ],
        ),
        migrations.CreateModel(
            name='Observation',
            fields=[
                ('observationTimeStamp', models.TextField(blank=True, verbose_name='observationTimeStamp')),
                ('observationDbId', models.TextField(primary_key=True, serialize=False, verbose_name='observationDbId')),
                ('collector', models.TextField(blank=True, verbose_name='collector')),
                ('value', models.TextField(blank=True, verbose_name='value')),
                ('cropDbId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jsonapi.Crop', verbose_name='cropDbId')),
            ],
        ),
        migrations.CreateModel(
            name='ObservationUnit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('observationUnitDbId', models.TextField(unique=True, verbose_name='observationUnitDbId')),
                ('name', models.TextField(verbose_name='name')),
                ('observationUnitLevel', models.TextField(blank=True, verbose_name='observationUnitLevel')),
                ('observationUnitLevels', models.TextField(blank=True, verbose_name='observationUnitLevels')),
                ('entryNumber', models.TextField(blank=True, verbose_name='entryNumber')),
                ('entryType', models.TextField(blank=True, verbose_name='entryType')),
                ('plotNumber', models.TextField(blank=True, verbose_name='plotNumber')),
                ('blockNumber', models.TextField(blank=True, verbose_name='blockNumber')),
                ('plantNumber', models.TextField(blank=True, verbose_name='plantNumber')),
                ('x', models.TextField(blank=True, verbose_name='x')),
                ('y', models.TextField(blank=True, verbose_name='y')),
                ('replicate', models.TextField(blank=True, verbose_name='replicate')),
                ('cropDbId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jsonapi.Crop', verbose_name='cropDbId')),
                ('germplasmDbId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jsonapi.Germplasm', verbose_name='germplasmDbId')),
            ],
        ),
        migrations.CreateModel(
            name='ObservationUnitTreatment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('factor', models.TextField(verbose_name='factor')),
                ('modality', models.TextField(verbose_name='modality')),
                ('cropDbId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jsonapi.Crop', verbose_name='cropDbId')),
                ('observationUnitDbId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jsonapi.ObservationUnit', verbose_name='observationUnitDbId')),
            ],
        ),
        migrations.CreateModel(
            name='ObservationUnitXref',
            fields=[
                ('source', models.TextField(verbose_name='source')),
                ('id', models.TextField(primary_key=True, serialize=False, verbose_name='id')),
                ('cropDbId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jsonapi.Crop', verbose_name='cropDbId')),
                ('observationUnitDbId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jsonapi.ObservationUnit', verbose_name='observationUnitDbId')),
            ],
        ),
        migrations.CreateModel(
            name='ObservationVariable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('observationVariableDbId', models.TextField(unique=True, verbose_name='observationVariableDbId')),
                ('cropDbId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jsonapi.Crop', verbose_name='cropDbId')),
                ('methodDbId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jsonapi.Method', verbose_name='methodDbId')),
            ],
        ),
        migrations.CreateModel(
            name='Ontology',
            fields=[
                ('ontologyDbId', models.TextField(primary_key=True, serialize=False, verbose_name='ontologyDbId')),
                ('cropDbId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jsonapi.Crop', verbose_name='cropDbId')),
            ],
        ),
        migrations.CreateModel(
            name='Pedigree',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pedigree', models.TextField(verbose_name='pedigree')),
                ('cropDbId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jsonapi.Crop', verbose_name='cropDbId')),
                ('germplasmDbId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pedigreeObject', to='jsonapi.Germplasm', verbose_name='germplasmDbId')),
                ('parent1Id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pedigreeChild1', to='jsonapi.Germplasm', verbose_name='parent1Id')),
                ('parent2Id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pedigreeChild2', to='jsonapi.Germplasm', verbose_name='parent2Id')),
            ],
        ),
        migrations.CreateModel(
            name='Program',
            fields=[
                ('programDbId', models.TextField(primary_key=True, serialize=False, verbose_name='programDbId')),
                ('name', models.TextField(verbose_name='name')),
                ('abbreviation', models.TextField(blank=True, verbose_name='abbreviation')),
                ('objective', models.TextField(blank=True, verbose_name='objective')),
                ('leadPerson', models.TextField(blank=True, verbose_name='leadPerson')),
                ('cropDbId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jsonapi.Crop', verbose_name='cropDbId')),
            ],
        ),
        migrations.CreateModel(
            name='Sample',
            fields=[
                ('sampleDbId', models.TextField(primary_key=True, serialize=False, verbose_name='sampleDbId')),
                ('cropDbId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jsonapi.Crop', verbose_name='cropDbId')),
            ],
        ),
        migrations.CreateModel(
            name='Scale',
            fields=[
                ('scaleDbId', models.TextField(primary_key=True, serialize=False, verbose_name='scaleDbId')),
                ('cropDbId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jsonapi.Crop', verbose_name='cropDbId')),
            ],
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('seasonDbId', models.TextField(primary_key=True, serialize=False, verbose_name='seasonDbId')),
                ('year', models.TextField(blank=True, verbose_name='year')),
                ('season', models.TextField(blank=True, verbose_name='season')),
                ('cropDbId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jsonapi.Crop', verbose_name='cropDbId')),
            ],
        ),
        migrations.CreateModel(
            name='Study',
            fields=[
                ('studyDbId', models.TextField(primary_key=True, serialize=False, verbose_name='studyDbId')),
                ('name', models.TextField(verbose_name='name')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('startDate', models.TextField(blank=True, verbose_name='startDate')),
                ('endDate', models.TextField(blank=True, verbose_name='endDate')),
                ('active', models.NullBooleanField(verbose_name='active')),
                ('license', models.TextField(blank=True, verbose_name='license')),
                ('lastUpdateVersion', models.TextField(blank=True, verbose_name='lastUpdateVersion')),
                ('lastUpdateTimestamp', models.TextField(blank=True, verbose_name='lastUpdateTimestamp')),
                ('cropDbId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jsonapi.Crop', verbose_name='cropDbId')),
                ('locationDbId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jsonapi.Location', verbose_name='locationDbId')),
            ],
        ),
        migrations.CreateModel(
            name='StudyAdditionalInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.TextField(verbose_name='key')),
                ('value', models.TextField(verbose_name='value')),
                ('cropDbId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jsonapi.Crop', verbose_name='cropDbId')),
                ('studyDbId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jsonapi.Study', verbose_name='studyDbId')),
            ],
        ),
        migrations.CreateModel(
            name='StudyContact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contactDbId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jsonapi.Contact', verbose_name='contactDbId')),
                ('cropDbId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jsonapi.Crop', verbose_name='cropDbId')),
                ('studyDbId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jsonapi.Study', verbose_name='studyDbId')),
            ],
        ),
        migrations.CreateModel(
            name='StudyDataLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(blank=True, verbose_name='name')),
                ('type', models.TextField(blank=True, verbose_name='type')),
                ('url', models.TextField(verbose_name='url')),
                ('cropDbId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jsonapi.Crop', verbose_name='cropDbId')),
                ('studyDbId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jsonapi.Study', verbose_name='studyDbId')),
            ],
        ),
        migrations.CreateModel(
            name='StudySeason',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cropDbId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jsonapi.Crop', verbose_name='cropDbId')),
                ('seasonDbId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jsonapi.Season', verbose_name='seasonDbId')),
                ('studyDbId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jsonapi.Study', verbose_name='studyDbId')),
            ],
        ),
        migrations.CreateModel(
            name='StudyType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(unique=True, verbose_name='name')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('cropDbId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jsonapi.Crop', verbose_name='cropDbId')),
            ],
        ),
        migrations.CreateModel(
            name='TaxonXref',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('taxonDbId', models.TextField(unique=True, verbose_name='taxonDbId')),
                ('source', models.TextField(verbose_name='source')),
                ('rank', models.TextField(blank=True, verbose_name='rank')),
                ('cropDbId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jsonapi.Crop', verbose_name='cropDbId')),
            ],
        ),
        migrations.CreateModel(
            name='TaxonXrefGermplasm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cropDbId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jsonapi.Crop', verbose_name='cropDbId')),
                ('germplasmDbId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jsonapi.Germplasm', verbose_name='germplasmDbId')),
                ('taxonDbId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jsonapi.TaxonXref', verbose_name='taxonDbId')),
            ],
        ),
        migrations.CreateModel(
            name='Trait',
            fields=[
                ('traitDbId', models.TextField(primary_key=True, serialize=False, verbose_name='traitDbId')),
                ('cropDbId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jsonapi.Crop', verbose_name='cropDbId')),
            ],
        ),
        migrations.CreateModel(
            name='Trial',
            fields=[
                ('trialDbId', models.TextField(primary_key=True, serialize=False, verbose_name='trialDbId')),
                ('name', models.TextField(verbose_name='name')),
                ('startDate', models.TextField(blank=True, verbose_name='startDate')),
                ('endDate', models.TextField(blank=True, verbose_name='endDate')),
                ('active', models.NullBooleanField(verbose_name='active')),
                ('datasetAuthorshipLicence', models.TextField(blank=True, verbose_name='datasetAuthorshipLicence')),
                ('datasetAuthorshipDatasetPUI', models.TextField(blank=True, verbose_name='datasetAuthorshipDatasetPUI')),
                ('cropDbId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jsonapi.Crop', verbose_name='cropDbId')),
                ('programDbId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jsonapi.Program', verbose_name='programDbId')),
            ],
        ),
        migrations.CreateModel(
            name='TrialAdditionalInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.TextField(verbose_name='key')),
                ('value', models.TextField(verbose_name='value')),
                ('cropDbId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jsonapi.Crop', verbose_name='cropDbId')),
                ('trialDbId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jsonapi.Trial', verbose_name='trialDbId')),
            ],
        ),
        migrations.CreateModel(
            name='TrialContact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contactDbId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jsonapi.Contact', verbose_name='contactDbId')),
                ('cropDbId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jsonapi.Crop', verbose_name='cropDbId')),
                ('trialDbId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jsonapi.Trial', verbose_name='trialDbId')),
            ],
        ),
        migrations.AddField(
            model_name='study',
            name='studyType',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jsonapi.StudyType', verbose_name='studyType'),
        ),
        migrations.AddField(
            model_name='study',
            name='trialDbId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jsonapi.Trial', verbose_name='trialDbId'),
        ),
        migrations.AddField(
            model_name='observationvariable',
            name='ontologyDbId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jsonapi.Ontology', verbose_name='ontologyDbId'),
        ),
        migrations.AddField(
            model_name='observationvariable',
            name='scaleDbId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jsonapi.Scale', verbose_name='scaleDbId'),
        ),
        migrations.AddField(
            model_name='observationvariable',
            name='traitDbId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jsonapi.Trait', verbose_name='traitDbId'),
        ),
        migrations.AddField(
            model_name='observationunit',
            name='studyDbId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jsonapi.Study', verbose_name='studyDbId'),
        ),
        migrations.AddField(
            model_name='observation',
            name='observationUnitDbId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jsonapi.ObservationUnit', verbose_name='observationUnitDbId'),
        ),
        migrations.AddField(
            model_name='observation',
            name='observationVariableDbId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jsonapi.ObservationVariable', verbose_name='observationVariableDbId'),
        ),
        migrations.AddField(
            model_name='observation',
            name='seasonDbId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jsonapi.Season', verbose_name='seasonDbId'),
        ),
        migrations.AddField(
            model_name='germplasmattribute',
            name='attributeCategoryDbId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jsonapi.GermplasmAttributeCategory', verbose_name='attributeCategoryDbId'),
        ),
        migrations.AddField(
            model_name='germplasmattribute',
            name='cropDbId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jsonapi.Crop', verbose_name='cropDbId'),
        ),
        migrations.AddField(
            model_name='donor',
            name='germplasmDbId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jsonapi.Germplasm', verbose_name='germplasmDbId'),
        ),
        migrations.AddField(
            model_name='contact',
            name='cropDbId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jsonapi.Crop', verbose_name='cropDbId'),
        ),
    ]
