from django.core.exceptions import ValidationError
from django.shortcuts import render
from .serializers import JobSerializer, NodeSerializer, EdgeSerializer
from .models import Job, Node, Edge
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from .tree_helper import parse_newick_tree


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
        data = JSONParser().parse(request)
        serializer = JobSerializer(data=data)
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
        if not nodes or not edges:
            nodes, edges = parse_newick_tree()
            node_serializer = NodeSerializer(data=nodes, many=True)
            if node_serializer.is_valid():
                node_serializer.save()
            edge_serializer = EdgeSerializer(data=edges, many=True)
            if edge_serializer.is_valid():
                edge_serializer.save()
        tree = {"nodes": nodes, "edges": edges}
        return JsonResponse(tree, status=status.HTTP_200_OK)