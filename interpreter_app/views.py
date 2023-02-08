from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
import json
from django.views.decorators.csrf import csrf_exempt
from interpreter.code_entities import CodeInternal

@csrf_exempt
def index(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        return render(request, "index.html")
    elif request.method == "POST":
        data: dict[str, str] = json.loads(request.body.decode())
        return HttpResponse(json.dumps({
            "output": CodeInternal(data['code'], data['input']).run()
        }))
    return HttpResponse("")