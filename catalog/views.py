import datetime
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

def hello_world(request: HttpRequest, unique_number: int) -> HttpResponse:
    now = datetime.datetime.now()
    print(f"Request params: {request.GET}")
    return HttpResponse(
        "<html>"
        "<h1>"
        "Hello World!"
        f"<h4>Unique number:{unique_number}</h4>"
        "</h1>"
        "</html>"
    )
