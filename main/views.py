from http.client import HTTPResponse
from sqlite3 import IntegrityError
from django.shortcuts import render
from .models import EarlyAccess
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

# Create your views here.
def index(request):
    return render(request, "main/index.html")

def form(request):
    if request.method == "GET":
        return render(request, "main/form.html")

    if request.method == "POST":
        name = request.POST["name"]
        email = request.POST["email"]
        fee = request.POST["fee"]
        news = request.POST.get("news")

        print(news)

        if name == "" or email == "" or fee == "" or news == "":
            return HttpResponseRedirect(reverse("error"))

        try:
            EarlyAccess.objects.create(
                name=name,
                email=email,
                fee=fee,
                news= "no" if news == None else "yes"
            )
        except IntegrityError:
            return HttpResponseRedirect(reverse("error"))

        return HttpResponseRedirect(reverse("success"))


def success(request):
    return render(request, "main/success.html")

def error(request):
    return render(request, "main/error.html")


