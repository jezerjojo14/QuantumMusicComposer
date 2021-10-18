from django.shortcuts import render
from . import quantum_program
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
import json
from django.views.decorators.csrf import ensure_csrf_cookie

# Create your views here.

def index(request):
    return render(request, "composerapp/index.html")

def generate_composition(request):
    post_data = json.loads(request.body.decode("utf-8"))
    print(post_data)
    data=quantum_program.generate_composition(post_data["mood"])
    # data={"C4": [8,9], "D4": [7,10,13,14], "E4": [0, 1, 6, 11, 12], "F4": [2,5], "G4": [3,4]}
    return JsonResponse(data)

@ensure_csrf_cookie
def result(request, mood, tempo):
    return render(request, "composerapp/result.html", {"preferences": json.dumps({"mood": mood, "tempo": tempo})})
