from django.urls import path
from .views import index_view  # the view responsible for the frontend

urlpatterns = [
    path('', index_view),  # add the view to the url
]