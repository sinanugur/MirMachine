from django.core.exceptions import ValidationError
from django.shortcuts import render
from .serializers import JobSerializer, NodeSerializer, EdgeSerializer, FamilySerializer
from .models import Job, Node, Edge, Family
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import status
from rest_framework.decorators import api_view
from .tree_helper import parse_newick_tree
from .family_importer import import_all_families
import hashlib


# Create your views here.
@ensure_csrf_cookie
def index_view(request, *args, **kwargs):
    return render(request, 'frontend/index.html', context={}, status=200)


@api_view(['GET'])
def get_job(request, id):
    if request.method == 'GET':
        try:
            job = Job.objects.get(id=id)
            serializer = JobSerializer(job)
            return JsonResponse(serializer.data)
        except ValidationError:
            response = {"message": "Not a valid UUID"}
            return JsonResponse(response,
                                status=status.HTTP_400_BAD_REQUEST)
        except:
            response = {"message": "Object does not exist in database"}
            return JsonResponse(response,
                                status=status.HTTP_404_NOT_FOUND)


# remember to remove exemptions
@api_view(['POST','GET'])
def post_job(request):
    if request.method == 'POST':
        serializer = JobSerializer(data=request.data)
        serializer.initial_data['hash'] = hashlib.md5(serializer.initial_data['data'].encode()).hexdigest()
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        jobs = Job.objects.all()
        serializer = JobSerializer(jobs, many=True)
        return JsonResponse(serializer.data, safe=False)


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
        families = Family.objects.all()
        serializer = FamilySerializer(families, many=True)
        if not families:
            families = import_all_families()
            serializer = FamilySerializer(data=families, many=True)
            if serializer.is_valid():
                serializer.save()
        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)