import sys

from django.core.exceptions import ValidationError
from django.shortcuts import render
from .serializers import JobSerializer
from .models import Job
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view


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
