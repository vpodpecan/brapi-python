import json

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView, View
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from jsonapi import serializers, models

DEF_PAGE_SIZE = 1000
HTTP_BAD_REQUEST_CODE = 400
JSON_POST_ARGS = 'jsonparams'


class JSONResponseMixin(object):
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

    def check_GET_parameters(self, pdict):
        return set(pdict.keys()) - set(self.get_parameters)

    def check_POST_parameters(self, pdict):
        return set(pdict.keys()) - set(self.post_json_parameters)

    def get_objects_GET(self, requestDict):
        raise NotImplementedError

    def get_objects_POST(self, requestDict):
        raise NotImplementedError

    def get(self, request, *args, **kwargs):
        requestDict = self.request.GET

        # sanity: fail if there are unwanted parameters
        unknownParams = self.check_parameters(requestDict)
        if unknownParams:
            return self.buildErrorResponse('Invalid query pararameter(s) {}'.format(unknownParams), HTTP_BAD_REQUEST_CODE)

        # execute query and make pagination
        objects = self.get_objects_GET(requestDict)
        # try:
        #     objects = self.get_objects(kwargs)
        # except Exception as e:
        #     return self.buildErrorResponse('Data error: {}'.format(str(e)), HTTP_BAD_REQUEST_CODE)

        try:
            pagesize = int(requestDict.get('pageSize', DEF_PAGE_SIZE))
            page = int(requestDict.get('page', 0)) + 1  # BRAPI wants zero page indexing...
        except:
            return self.buildErrorResponse('Invalid page or pageSize parameter', HTTP_BAD_REQUEST_CODE)

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
            data.append(self.serializer(obj).data)
        return JsonResponse(self.buildResponse(results={'data': data}, pagination=pagination))
# end


class JSONURLResponseMixinDetails(JSONResponseMixin):
    def get(self, request, *args, **kwargs):
        requestDict = kwargs
        try:
            pkval = requestDict.get(self.pk)
            obj = self.model.objects.get(pk=pkval)
        except self.model.DoesNotExist:
            return self.buildErrorResponse('Invalid object ID', 404)

        serializer = self.serializer(obj)
        return JsonResponse(self.buildResponse(results=serializer.data))


# class JSONResponseMixinDetails(JSONResponseMixin):
#     def get(self, request, *args, **kwargs):
#         requestDict = request.GET
#         print(requestDict)
#         print(args)
#         print(kwargs)
#         input()
#         try:
#             pkval = requestDict.get(self.pk)
#             obj = self.model.objects.get(pk=pkval)
#         except self.model.DoesNotExist:
#             return self.buildErrorResponse('Invalid object ID', 404)
#
#         serializer = self.serializer(obj)
#         return JsonResponse(self.buildResponse(results=serializer.data))


class JSONPOSTResponseMixin(JSONResponseMixin):
    # forward the parameters
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body.decode("utf-8"))
        except Exception:
            return self.buildErrorResponse('Invalid JSON POST parameters', HTTP_BAD_REQUEST_CODE)

        context = {}
        return JsonResponse(self.get_data(context, **{JSON_POST_ARGS: data}))

    def check_parameters(self, pdict):
        return set(pdict.keys()) - set(self.post_json_parameters)


@method_decorator(csrf_exempt, name='dispatch')
class UnsafeTemplateView(View):
    pass


class Index(TemplateView):
    def get(self, request):
        return self.post(request)

    def post(self, request):
        return HttpResponse("BRAPI API")


class GermplasmDetails(JSONURLResponseMixinDetails, UnsafeTemplateView):
    model = models.Germplasm
    serializer = serializers.GermplasmDetailsSerializer
    pk = 'germplasmDbId'


class GermplasmSearch(JSONPOSTResponseMixin, UnsafeTemplateView):
    model = models.Germplasm
    serializer = serializers.GermplasmDetailsSerializer
    get_parameters = ['germplasmName', 'germplasmDbId', 'germplasmPUI']
    post_json_parameters = ['germplasmPUIs', 'germplasmDbIds', 'germplasmSpecies', 'germplasmGenus', 'germplasmNames', 'accessionNumbers']

    # TODO get_POST_objects, get_GET_objects


    def get_objects(self, requestDict):
        objects = self.model.objects.all()
        param2attr = {'germplasmPUIs': 'germplasmPUI',
                      'germplasmDbIds': 'germplasmDbId',
                      'germplasmSpecies': 'species',
                      'germplasmGenus': 'genus',
                      'germplasmNames': 'name',
                      'accessionNumbers': 'accessionNumber'}
        for p in param2attr:
            if p in requestDict:
                kw = '{}__in'.format(param2attr[p])
                objects = objects.filter(**{kw: requestDict[p]})
        return objects


class ProgramList(JSONResponseMixin, TemplateView):
    model = models.Program
    serializer = serializers.ProgramSerializer
    get_parameters = ['programName', 'abbreviation']

    def get_objects(self, requestDict):
        objects = self.model.objects.all()
        if 'programName' in requestDict:
            objects = objects.filter(name=requestDict['programName'])
        if 'abbreviation' in requestDict:
            objects = objects.filter(abbreviation=requestDict['abbreviation'])
        return objects


class TrialDetails(JSONResponseMixinDetails, TemplateView):
    model = models.Trial
    serializer = serializers.TrialDetailsSerializer
    pk = 'trialDbId'


class TrialList(JSONResponseMixin, TemplateView):
    model = models.Trial
    serializer = serializers.TrialDetailsSerializer
    get_parameters = ['programDbId', 'locationDbId', 'active', ]

    def get_objects(self, kwargs):
        if 'locationDbId' in kwargs:
            studies = models.Study.objects.filter(locationDbId=kwargs['locationDbId'])
            # objects =

            models.Trial.objects.filter(locationDbId__in=studies)
        else:
            objects = self.model.objects
        return objects.filter(**kwargs)

#objects = self.model.objects.filter(**kwargs)
#     studies = models.Study.objects.filter(locationDbId=locationDbId)
#     trials = models.Trial.objects.filter()
