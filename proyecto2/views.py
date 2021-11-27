from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

# from .invertedindex.index import inverse_index
import os.path
import glob
from pathlib import Path
import json
from django.http import JsonResponse, StreamingHttpResponse


# from os.path import join
# index = inverse_index()
# if not os.path.isfile("index"):
#   index.from_json(glob.glob("../data_elecciones/*.json"))
#   index.dump()
# else:
#   index.load()

def mainpage(request):
  return render(request,'index.html')

def dashboard(request):
  return render(request, 'dashboard.html')

@csrf_exempt
def invertedindexquery(request):
  data = json.loads(request.body)
  retorno = []
  text = data['query']
  i = 0

  retorno = cosine(text)
  # for id in index.query(text):
    #   retorno.append(str(id))
  #   if i == 5:
  #       break
  #   i = i + 1
  return JsonResponse(json.dumps(retorno) , safe=False)
