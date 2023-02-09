from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
import json
from django.views.decorators.csrf import csrf_exempt
from interpreter.legacy.code_entities import CodeInternal

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

@csrf_exempt
def syntax(request: HttpRequest) -> HttpResponse:
    with open('static/Syntax.pdf', 'rb') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline;filename=Syntax.pdf'
        return response