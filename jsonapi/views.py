import json
from ast import literal_eval
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView, View
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.core.exceptions import FieldDoesNotExist
from django_extensions.management.commands import show_urls
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from jsonapi import serializers, models

DEF_PAGE_SIZE = 1000
HTTP_BAD_REQUEST_CODE = 400
JSON_POST_ARGS = 'jsonparams'


class JSONResponseMixin(object):
    pagination_params = ['page', 'pageSize']

    def buildErrorResponse(self, message, code):
        err = {"metadata": {
                "pagination": {
                    "pageSize": 0,
                    "currentPage": 0,
                    "totalCount": 0,
                    "totalPages": 0
                },
                "status": [{
                    "message": message,
                    "code": code
                }],
                "datafiles": []
            },
            "result": {}
        }
        return err

    def buildResponse(self, results, pagination={"pageSize": 0, "currentPage": 0, "totalCount": 0, "totalPages": 0}, status=[], datafiles=[]):
        output = {}
        output['result'] = results
        output['metadata'] = {}
        output['metadata']['pagination'] = pagination
        output['metadata']['status'] = status
        output['metadata']['datafiles'] = datafiles
        return output

    def prepareResponse(self, objects, requestDict):
        try:
            pagesize = int(requestDict.get('pageSize', DEF_PAGE_SIZE))
            page = int(requestDict.get('page', 0)) + 1  # BRAPI wants zero page indexing...
        except:
            return self.buildErrorResponse('Invalid page or pageSize parameter', HTTP_BAD_REQUEST_CODE)

        # order is mandatory because of pagination
        if self.model and not objects.ordered:
            objects = objects.order_by('pk')

        paginator = Paginator(objects, pagesize)
        try:
            pageObjects = paginator.page(page)
        except EmptyPage:
            # If page is out of range, deliver last page of results.
            return self.buildErrorResponse('Empty page was requested: {}'.format(page-1), HTTP_BAD_REQUEST_CODE)
            # pageObjects = paginator.page(paginator.num_pages)
        pagination = {'pageSize': pagesize,
                      'currentPage': page-1,
                      'totalCount': len(objects),
                      'totalPages': paginator.num_pages
                      }

        # return serialized data
        data = []
        for obj in pageObjects:
            if self.serializer:
                data.append(self.serializer(obj).data)
            else:
                data.append(obj)
        return self.buildResponse(results={'data': data}, pagination=pagination)

    def sortOrder(self, requestDict, objects):
        val = requestDict.get('sortOrder')
        if val is not None:
            val = val.lower()
            if val == 'desc':
                objects = objects.reverse()
            elif val == 'asc':
                pass  # by default
            else:
                raise ValueError('Invalid value for "sortOrder" parameter: {}'.format(val))
        return objects


@method_decorator(csrf_exempt, name='dispatch')
class UnsafeTemplateView(View):
    pass


# we have to handle different types of requests:
# GET with parameters in URL path e.g., ... brapi/v1/germplasm/id
# GET with parameters encoded as "application/x-www-form-urlencoded"
# POST with parameters encoded as "application/json"
#
# in addition there is a shortcut class GET_detail_response for listing single objects by PK

class GET_response(JSONResponseMixin):
    def checkGETparameters(self, requestDict):
        return set(requestDict.keys()) - set(self.get_parameters) - set(self.pagination_params)

    def get(self, request, *args, **kwargs):
        requestDict = self.request.GET

        # sanity: fail if there are unwanted parameters
        unknownParams = self.checkGETparameters(requestDict)
        if unknownParams:
            return JsonResponse(self.buildErrorResponse('Invalid query pararameter(s) {}'.format(unknownParams), HTTP_BAD_REQUEST_CODE))

        # execute query and make pagination
        objects = self.get_objects_GET(requestDict)
        # try:
        #     objects = self.get_objects_GET(requestDict)
        # except Exception as e:
        #     return JsonResponse(self.buildErrorResponse('Data error: {}'.format(str(e)), HTTP_BAD_REQUEST_CODE))

        response = self.prepareResponse(objects, requestDict)
        return JsonResponse(response)


class POST_JSON_response(JSONResponseMixin):
    def checkPOSTparameters(self, requestDict):
        return set(requestDict.keys()) - set(self.post_json_parameters) - set(self.pagination_params)

    def post(self, request, *args, **kwargs):
        try:
            requestDict = json.loads(request.body.decode("utf-8"))
        except Exception:
            return JsonResponse(self.buildErrorResponse('Invalid JSON POST parameters', HTTP_BAD_REQUEST_CODE))

        unknownParams = self.checkPOSTparameters(requestDict)
        if unknownParams:
            return JsonResponse(self.buildErrorResponse('Invalid query pararameter(s) {}'.format(unknownParams), HTTP_BAD_REQUEST_CODE))

        # execute query and make pagination
        try:
            objects = self.get_objects_POST(requestDict)
        except Exception as e:
            return JsonResponse(self.buildErrorResponse('Data error: {}'.format(str(e)), HTTP_BAD_REQUEST_CODE))

        response = self.prepareResponse(objects, requestDict)
        return JsonResponse(response)


class GET_URLPARAMS_response(JSONResponseMixin):
    def checkGETparameters(self, requestDict):
        return set(requestDict.keys()) - set(self.get_parameters) - set(self.pagination_params)

    def get(self, request, *args, **kwargs):
        requestDict = self.request.GET

        # sanity: fail if there are unwanted parameters
        unknownParams = self.checkGETparameters(requestDict)
        if unknownParams:
            return JsonResponse(self.buildErrorResponse('Invalid query pararameter(s) {}'.format(unknownParams), HTTP_BAD_REQUEST_CODE))

        # execute query and make pagination
        try:
            objects = self.get_objects_GET(requestDict, **kwargs)
        except Exception as e:
            return JsonResponse(self.buildErrorResponse('Data error: {}'.format(str(e)), HTTP_BAD_REQUEST_CODE))

        response = self.prepareResponse(objects, requestDict)
        return JsonResponse(response)


class GET_detail_response(JSONResponseMixin):
    def get(self, request, *args, **kwargs):
        requestDict = kwargs
        try:
            pkval = requestDict.get(self.pk)
            obj = self.model.objects.get(pk=pkval)
        except self.model.DoesNotExist:
            return JsonResponse(self.buildErrorResponse('Invalid object ID', 404))

        serializer = self.serializer(obj)
        return JsonResponse(self.buildResponse(results=serializer.data))


class Index(TemplateView):
    template_name = 'root.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        return self.get(request)


class CallSearch(GET_response, UnsafeTemplateView):
    model = None
    serializer = None
    get_parameters = ['datatype']

    def get_objects_GET(self, requestDict):
        datatype = requestDict.get('datatype')

        tmp = [x.split('\t') for x in show_urls.Command().handle(format_style='dense', urlconf='ROOT_URLCONF', no_color=True).split('\n')]
        urls = []
        for entry in tmp:
            if len(entry) < 2:
                continue
            url = entry[0]
            viewclass = entry[1].split('.')[-1]
            if url.startswith('/brapi/v1/'):
                url = url.replace('/brapi/v1/', '').replace('<', '{').replace('>', '}')
                if url:
                    urls.append((url, globals()[viewclass]))
        result = []
        for url, klas in urls:
            data = {}
            data['call'] = url
            data['datatypes'] = ['json']
            data['methods'] = []
            if issubclass(klas, GET_response) or issubclass(klas, GET_URLPARAMS_response) or issubclass(klas, GET_detail_response):
                data['methods'].append('GET')
            if issubclass(klas, POST_JSON_response):
                data['methods'].append('POST')

            if datatype is None or datatype in data['datatypes']:
                result.append(data)
        return result


class GermplasmDetails(GET_detail_response, UnsafeTemplateView):
    model = models.Germplasm
    serializer = serializers.GermplasmDetailsSerializer
    pk = 'germplasmDbId'


class GermplasmSearch(GET_response, POST_JSON_response, UnsafeTemplateView):
    model = models.Germplasm
    serializer = serializers.GermplasmDetailsSerializer
    get_parameters = ['germplasmName', 'germplasmDbId', 'germplasmPUI']
    post_json_parameters = ['germplasmPUIs', 'germplasmDbIds', 'germplasmSpecies', 'germplasmGenus', 'germplasmNames', 'accessionNumbers']

    def get_objects_GET(self, requestDict):
        qdict = {}
        for param in self.get_parameters:
            if param in requestDict:
                qdict[param] = requestDict[param]
        return self.model.objects.filter(Q(**qdict))

    def get_objects_POST(self, requestDict):
        qdict = {}
        param2attr = {'germplasmPUIs': 'germplasmPUI',
                      'germplasmDbIds': 'germplasmDbId',
                      'germplasmSpecies': 'species',
                      'germplasmGenus': 'genus',
                      'germplasmNames': 'name',
                      'accessionNumbers': 'accessionNumber'}
        for p in param2attr:
            if p in requestDict:
                qdict['{}__in'.format(param2attr[p])] = requestDict[p]
        return self.model.objects.filter(Q(**qdict))


class ProgramList(GET_response, TemplateView):
    model = models.Program
    serializer = serializers.ProgramSerializer
    get_parameters = ['programName', 'abbreviation']

    def get_objects_GET(self, requestDict):
        query = Q()
        if 'programName' in requestDict:
            query &= Q(name=requestDict['programName'])
        if 'abbreviation' in requestDict:
            query &= Q(abbreviation=requestDict['abbreviation'])

        objects = self.model.objects.filter(query)
        return objects


class TrialDetails(GET_detail_response, TemplateView):
    model = models.Trial
    serializer = serializers.TrialDetailsSerializer
    pk = 'trialDbId'


class TrialList(GET_response, TemplateView):
    model = models.Trial
    serializer = serializers.TrialSummarySerializer
    get_parameters = ['programDbId', 'locationDbId', 'active', 'sortBy', 'sortOrder']

    def get_objects_GET(self, requestDict):
        query = Q()

        val = requestDict.get('programDbId')
        if val is not None:
            query &= Q(programDbId=val)

        val = requestDict.get('active')
        if val is not None:
            val = val.lower()
            if val not in ['true', 'false']:
                raise ValueError('Invalid value for "active" parameter: {}'.format(val))
            val = True if val == 'true' else False
            query &= Q(active=val)

        objects = self.model.objects.filter(query)

        # we have to handle most cases manually because the fields are renamed
        val = requestDict.get('sortBy')
        if val is not None:
            if val == 'trialName':
                objects = objects.order_by('name')
            elif val == 'programName':
                objects = objects.order_by('programDbId__name')
            elif val == 'studyName':
                objects = objects.order_by('study__name')
            elif val == 'locationName':
                objects = objects.order_by('study__locationDbId__name')
            else:
                try:
                    self.model._meta.get_field(val)
                    objects = objects.order_by(val)
                except:
                    raise ValueError('Invalid value for "sortBy" parameter: {}'.format(val))

        return self.sortOrder(requestDict, objects)


class StudyDetails(GET_detail_response, TemplateView):
    model = models.Study
    serializer = serializers.StudyDetailsSerializer
    pk = 'studyDbId'


class StudyList(GET_response, TemplateView):
    model = models.Study
    serializer = serializers.StudySummarySerializer
    get_parameters = []

    def get_objects_GET(self, requestDict):
        return self.model.objects.all()


class StudySearch(GET_response, POST_JSON_response, UnsafeTemplateView):
    model = models.Study
    serializer = serializers.StudySummarySerializer
    get_parameters = ['studyType', 'programDbId', 'locationDbId', 'seasonDbId', 'germplasmDbIds',
                      'observationVariableDbIds', 'active', 'sortBy', 'sortOrder']
    post_json_parameters = ['studyType', 'studyNames', 'studyLocations', 'programNames',
                            'germplasmDbIds', 'observationVariableDbIds', 'active', 'sortBy', 'sortOrder']

    # this is actual ListStudySummaries
    def get_objects_GET(self, requestDict):
        query = Q()
        distinct = False

        val = requestDict.get('studyType')
        if val is not None:
            query &= Q(studyType__name=val)

        val = requestDict.get('programDbId')
        if val is not None:
            query &= Q(trialDbId__programDbId__pk=val)

        val = requestDict.get('locationDbId')
        if val is not None:
            query &= Q(locationDbId__pk=val)

        val = requestDict.get('seasonDbId')
        if val is not None:
            # the API doc is idiotic about this: seasonDbId can be either PK or year...
            query &= (Q(studyseason__seasonDbId__pk=val) | Q(studyseason__seasonDbId__year=val))
            distinct = True

        val = requestDict.get('germplasmDbIds')
        if val is not None:
            # safely parse list of strings
            try:
                val = literal_eval(val)
            except:
                raise ValueError('Invalid value for "germplasmDbIds" parameter: {}'.format(val))
            query &= Q(cropDbId__germplasm__pk__in=val)
            distinct = True

        val = requestDict.get('observationVariableDbIds')
        if val is not None:
            # safely parse list of strings
            try:
                val = literal_eval(val)
            except:
                raise ValueError('Invalid value for "observationVariableDbIds" parameter: {}'.format(val))
            query &= Q(cropDbId__observationvariable__pk__in=val)
            distinct = True

        val = requestDict.get('active')
        if val is not None:
            val = val.lower()
            if val not in ['true', 'false']:
                raise ValueError('Invalid value for "active" parameter: {}'.format(val))
            val = True if val == 'true' else False
            query &= Q(active=val)

        val = requestDict.get('sortBy')
        orderAttr = None
        if val is not None:
            try:
                self.model._meta.get_field(val)
                orderAttr = val
            except:
                raise ValueError('Invalid value for "sortBy" parameter: {}'.format(val))

        objects = self.model.objects.filter(query)
        if distinct:
            objects = objects.distinct()
        if orderAttr:
            objects = objects.order_by(orderAttr)

        return self.sortOrder(requestDict, objects)

    def get_objects_POST(self, requestDict):
        query = Q()
        distinct = False

        val = requestDict.get('studyType')
        if val is not None:
            query &= Q(studyType=val)

        val = requestDict.get('studyNames')
        if val is not None:
            query &= Q(name__in=val)

        val = requestDict.get('studyLocations')
        if val is not None:
            query &= Q(locationDbId__name__in=val)

        val = requestDict.get('programNames')
        if val is not None:
            query &= Q(trialDbId__programDbId__name__in=val)

        val = requestDict.get('germplasmDbIds')
        if val is not None:
            query &= Q(cropDbId__germplasm__pk__in=val)
            distinct = True

        val = requestDict.get('observationVariableDbIds')
        if val is not None:
            query &= Q(cropDbId__observationvariable__pk__in=val)
            distinct = True

        val = requestDict.get('active')
        if val is not None:
            val = val.lower()
            if val not in ['true', 'false']:
                raise ValueError('Invalid value for "active" parameter: {}'.format(val))
            val = True if val == 'true' else False
            query &= Q(active=val)

        val = requestDict.get('sortBy')
        orderAttr = None
        if val is not None:
            try:
                self.model._meta.get_field(val)
                orderAttr = val
            except:
                raise ValueError('Invalid value for "sortBy" parameter: {}'.format(val))

        objects = self.model.objects.filter(query)
        if distinct:
            objects = objects.distinct()
        if orderAttr:
            objects = objects.order_by(orderAttr)

        return self.sortOrder(requestDict, objects)


class StudyObservationVariable(GET_URLPARAMS_response, UnsafeTemplateView):
    model = models.ObservationVariable
    serializer = serializers.ObservationVariableSerializer
    get_parameters = []

    def get_objects_GET(self, requestDict, **kwargs):
        study = models.Study.objects.get(studyDbId=kwargs.get('studyDbId'))
        variables = study.cropDbId.observationvariable_set.all()
        return variables


class StudyGermplasm(GET_URLPARAMS_response, UnsafeTemplateView):
    model = models.Germplasm
    serializer = serializers.Study_GermplasmSerializer
    get_parameters = []

    def get_objects_GET(self, requestDict, **kwargs):
        study = models.Study.objects.get(studyDbId=kwargs.get('studyDbId'))
        return study.cropDbId.germplasm_set.all()


class LocationList(GET_response, UnsafeTemplateView):
    model = models.Location
    serializer = serializers.LocationSerializer
    get_parameters = ['locationType']

    def get_objects_GET(self, requestDict):
        query = Q()
        if 'locationType' in requestDict:
            query &= Q(type=requestDict['locationType'])

        objects = self.model.objects.filter(query)
        return objects


class LocationDetails(GET_detail_response, UnsafeTemplateView):
    model = models.Location
    serializer = serializers.LocationSerializer
    pk = 'locationDbId'
