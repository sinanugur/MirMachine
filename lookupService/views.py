from django.shortcuts import render


# Create your views here.
def index_view(request, *args, **kwargs):
    return render(request, 'frontend/index.html', context={}, status=200)
