from http.client import HTTPResponse
from sqlite3 import IntegrityError
from django.shortcuts import render
from .models import EarlyAccess
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from dashboard.models import Landing_Logs, application_Logs, unique_Logs
import random

# Create your views here.
def index(request):
    Landing_Logs.objects.create(
        landing_page = Landing_Logs.objects.last().landing_page + 1
    )
    
    if request.session.get('visit', False):
        unique_Logs.objects.create(
            unique = unique_Logs.objects.last().unique + 1
        )
    else:
        request.session['visit'] = True

    return render(request, "main/index.html")

def form(request):
    if request.method == "GET":
        application_Logs.objects.create(
            application_page = application_Logs.objects.last().application_page + 1
        )
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

def seed(request):

    data = [
        "aatechkadir@gmail.com",
        "ai.danyarotravelandtoursltd@gmail.com",
        "karamaabdullahi@gmail.com",
        "amaigishiripetroleum@gmail.com",
        "aattanigerialtd@gmail.com",
        "aadandinigltd@gmail.com",
        "dankd3000@gmail.com",
        "a.agundawa@gmail.com",
        "s.babaukowa@gmail.com",
        "aminubamalli@yahoo.com",
        "aaranoagro@gmail.com",
        "jibrinaliyulafalim@gmail.com",
        "aangorondutsepetroleum2020@gmail.com",
        "abypetroleum2@gmail.com",
        "adrabsenterprises@gmail.com",
        "ahsintl@hotmail.com",
        "bsmauramu@gmail.com",
        "abdullahikarama@gmail.com",
        "amkorau@yahoo.com",
        "magajiahmad11@gmail.com",
        "auwalusani64@gmail.com",
        "alisheshe123@gmail.com",
        "asaoilnigltd705@gmail.com",
        "aumaipampo@gmail.com",
        "auimultipurpose@yahoo.com",
        "aulbaluminium2@gmail.com",
        "auytransport5@gmail.com",
        "aymaikifioilandgas@gmail.com",
        "yhgama@gmail.com",
        "ayhcompanyltd@gmail.com"
    ]

    for i in range(6817):
        Landing_Logs.objects.create(
            landing_page = i
        )

    for i in range(291):
        application_Logs.objects.create(
            application_page = i
        )

    for i in range(5905):
        unique_Logs.objects.create(
            unique = i
        )

    for i in data:
        try:
            name = i.split('@')
            EarlyAccess.objects.create(
                name=name[0],
                email=i,
                fee= random.randint(10, 1000),
                news= random.choice(("no", "yes"))
            )
        except IntegrityError:
            return HttpResponseRedirect(reverse("error"))

    return HttpResponseRedirect(reverse("success"))

    

    


