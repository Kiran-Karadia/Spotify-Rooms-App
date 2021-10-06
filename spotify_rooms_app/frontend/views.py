from django.shortcuts import render

# Create your views here.

# To render the index.html template
def index(request, *args, **kwargs):
    return render(request, "frontend/index.html")