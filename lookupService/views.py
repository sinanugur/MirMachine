from django.core.exceptions import ValidationError
from django.shortcuts import render
from rest_framework.views import APIView
from lookupService.helpers.job_pre_processor import process_form_data, user_can_post
from lookupService.helpers.job_scheduler import schedule_job
from .serializers import NodeSerializer, \
    EdgeSerializer, FamilySerializer, NodeFamilyRelationSerializer, StrippedJobSerializer
from .models import Job, Node, Edge, Family, NodeFamilyRelation, Cookie
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import status
from rest_framework.decorators import api_view
from lookupService.helpers.tree_helper import parse_newick_tree
from lookupService.helpers.family_importer import import_all_families, import_node_to_family_db
from engine.scripts.mirmachine_args import show_node_families_args
from lookupService.helpers.result_parser import get_and_parse_results, zip_results
from lookupService.helpers.request_verifier import validate_job_exists_and_complete
from lookupService.helpers.maintainer import delete_job_data
from ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
from MirMachineWebapp import user_config as config
import json
import threading

stop_flag = False
job_thread = None


@ensure_csrf_cookie
def index_view(request, *args, **kwargs):
    return render(request, 'frontend/index.html', context={}, status=200)


@api_view(['GET'])
def get_job(request, _id):
    if request.method == 'GET':
        try:
            job = Job.objects.get(id=_id)
            serializer = StrippedJobSerializer(job)
            return JsonResponse(serializer.data)
        except ValidationError:
            response = {"message": "Not a valid UUID"}
            return JsonResponse(response,
                                status=status.HTTP_400_BAD_REQUEST)
        except:
            response = {"message": "Object does not exist in database"}
            return JsonResponse(response,
                                status=status.HTTP_404_NOT_FOUND)


class PostJob(APIView):
    @method_decorator(ratelimit(key='ip', rate=config.JOB_SUBMIT_THROTTLE_RATE, method='POST',
                                block=config.THROTTLE_JOB_SUBMIT))
    def post(self, request, format=None):
        try:
            if not user_can_post(request.COOKIES['csrftoken']):
                response = {"message": "You already have a queued or ongoing job, cancel it to add new"}
                return JsonResponse(response, status=status.HTTP_403_FORBIDDEN)
            serializer = process_form_data(request)
            if serializer.is_valid():
                instance = serializer.save()
                stripped = StrippedJobSerializer(instance)
                global job_thread
                global stop_flag
                if job_thread is None or not job_thread.is_alive():
                    job_thread = threading.Thread(target=schedule_job, args=(lambda: stop_flag,))
                    job_thread.start()
                return JsonResponse(stripped.data, status=status.HTTP_201_CREATED)
        except ValueError as e:
            response = {"message": str(e)}
            return JsonResponse(response, status=status.HTTP_404_NOT_FOUND)
        except RuntimeError:
            response = {"message": "Could not get genome from NCBI"}
            return JsonResponse(response, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except NameError:
            response = {"message": "Not a valid species name. Special characters are not allowed"}
            return JsonResponse(response, status=status.HTTP_400_BAD_REQUEST)
        except PermissionError as e:
            response = {"message": str(e)}
            return JsonResponse(response, status=status.HTTP_403_FORBIDDEN)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        try:
            params = request.query_params
            # print(params)
            job = Job.objects.get(id=params["id"])
            global stop_flag
            global job_thread
            if job.status == "ongoing" and job_thread is not None:
                stop_flag = True
                job_thread.join()
                delete_job_data(job)
                stop_flag = False
                job_thread = threading.Thread(target=schedule_job, args=(lambda: stop_flag,))
                job_thread.start()
            else:
                delete_job_data(job)
            response = {"message": "Job has been canceled and removed from the database"}
            return JsonResponse(response, status=status.HTTP_200_OK)
        except Job.DoesNotExist:
            response = {"message": "Object does not exist in database"}
            return JsonResponse(response,
                                status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_tree(request):
    if request.method == 'GET':
        nodes = Node.objects.all()
        edges = Edge.objects.all()
        node_serializer = NodeSerializer(nodes, many=True)
        edge_serializer = EdgeSerializer(edges, many=True)
        if not nodes or not edges:
            nodes, edges = parse_newick_tree()
            node_serializer = NodeSerializer(data=nodes, many=True)
            if node_serializer.is_valid():
                node_serializer.save()
            edge_serializer = EdgeSerializer(data=edges, many=True)
            if edge_serializer.is_valid():
                edge_serializer.save()
        tree = {"nodes": node_serializer.data, "edges": edge_serializer.data}
        return JsonResponse(tree, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_families(request):
    if request.method == 'GET':
        families = Family.objects.order_by('name')
        serializer = FamilySerializer(families, many=True)
        if not families:
            families = import_all_families()
            serializer = FamilySerializer(data=families, many=True)
            if serializer.is_valid():
                serializer.save()
        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)


@api_view(['GET'])
def get_included_families(request):
    if request.method == 'GET':
        params = request.query_params

        # parsing booleans
        both_ways = json.loads(params.get('both_ways'))
        single_node = json.loads(params.get('single_node'))
        relations = NodeFamilyRelation.objects.all()

        if not relations:
            relations = import_node_to_family_db()
            print(relations)
            serializer = NodeFamilyRelationSerializer(data=relations, many=True)
            if serializer.is_valid():
                serializer.save()
            else:
                print(serializer.errors)
        relations = NodeFamilyRelation.objects.all()
        if single_node:
            families = NodeFamilyRelation.objects.filter(node=params.get('node'))
            families = [e.family for e in families]
        else:
            families = show_node_families_args(both_ways, params.get('node'), relations)
        families.sort()
        response = {'families': families}
        return JsonResponse(response, status=status.HTTP_200_OK, safe=False)


@api_view(['GET'])
def get_results(request, _id):
    if request.method == 'GET':
        job_object = Job.objects.filter(id=_id)
        message = validate_job_exists_and_complete(job_object)
        if message != '':
            return JsonResponse(message, status=status.HTTP_400_BAD_REQUEST, safe=False)

        tag = job_object[0].species
        response = get_and_parse_results(tag)
        return JsonResponse(response, status=status.HTTP_200_OK)


@api_view(['GET'])
def download_results(request, _id):
    if request.method == 'GET':
        job_object = Job.objects.filter(id=_id)
        message = validate_job_exists_and_complete(job_object)
        if message != '':
            return JsonResponse(message, status=status.HTTP_400_BAD_REQUEST, safe=False)
        tag = job_object[0].species
        response = zip_results(tag)
        return response


@api_view(['GET'])
def check_if_new_client(request):
    if request.method == 'GET':
        cookie = request.COOKIES['csrftoken']
        if not Cookie.objects.filter(cookie=cookie):
            new = Cookie(cookie=cookie)
            new.save()
            response = {'message': 'new_user'}
            return JsonResponse(response, status=status.HTTP_200_OK)
        else:
            response = {'message': 'old_user'}
            return JsonResponse(response, status=status.HTTP_200_OK)


@api_view(['GET'])
def check_if_user_can_post(request):
    if request.method == 'GET':
        cookie = request.COOKIES['csrftoken']
        ability = user_can_post(cookie)
        response = {'message': ability}
        return JsonResponse(response, status=status.HTTP_200_OK)