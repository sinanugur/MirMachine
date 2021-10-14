from django.urls import path, re_path
from .views import get_job, PostJob, get_tree, get_families, get_included_families
from .consumers import MonitorConsumer

urlpatterns = [
    path('jobs/', PostJob.as_view()),
    path('job/<str:_id>', get_job),
    path('tree/', get_tree),
    path('families/', get_families),
    path('relations/', get_included_families)
]

websocket_patterns = [
    path('ws/job/<str:_id>', MonitorConsumer.as_asgi())
]