from django.urls import path
from .views import get_job, post_job


urlpatterns = [
    path('jobs/', post_job),
    path('job/<uuid:id>', get_job),
]