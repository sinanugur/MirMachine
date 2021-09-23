from django.urls import path
from .views import get_job, post_job, get_tree, get_families, get_included_families


urlpatterns = [
    path('jobs/', post_job),
    path('job/<str:_id>', get_job),
    path('tree/', get_tree),
    path('families/', get_families),
    path('relations/', get_included_families)
]