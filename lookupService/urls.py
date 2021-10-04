from django.urls import path, re_path
from .views import get_job, post_job, get_tree, get_families, get_included_families
from .consumers import MonitorConsumer

urlpatterns = [
    path('jobs/', post_job),
    path('job/<str:_id>', get_job),
    path('tree/', get_tree),
    path('families/', get_families),
    path('relations/', get_included_families)
]

websocket_patterns = [
    path('ws/job/<str:_id>', MonitorConsumer.as_asgi())
]