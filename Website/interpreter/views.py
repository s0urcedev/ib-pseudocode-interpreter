from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
import subprocess
import json
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def index(request):
    # if request.method == "GET":
    return render(request, "index.html")
    # elif request.method == "POST":
    #     data: dict[str, str] = json.loads(request.body.decode())
    #     sb: subprocess.CompletedProcess = subprocess.run(
    #         ['python', '../Interpreter/main.py'],
    #         input=f"{data['code']}\n{chr(3)}\n{data['input']}".encode(),
    #         capture_output=True
    #     )
    #     return HttpResponse(json.dumps({
    #         "stdout": sb.stdout.decode(),
    #         "stderr": sb.stderr.decode()
    #     }))
    return HttpResponse("")