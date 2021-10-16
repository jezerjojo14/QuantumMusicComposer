from django.shortcuts import render
from . import quantum_program
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse

# Create your views here.

def index(request):
    return render(request, "composerapp/index.html")

def generate_composition(request):
    post_data = json.loads(request.body.decode("utf-8"))
    args={}
    data=quantum_program.generate_composition(args)
    return JsonResponse(data)
