from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login, authenticate, logout
# from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Landing_Logs, application_Logs, unique_Logs, Wallet, User
from main.models import EarlyAccess

# Create your views here.
def index(request):
    if request.method == "GET":
        return render(request, "dashboard/login.html")

    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        user = authenticate(username=email, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("dashhome"))
        else:
            return HttpResponseRedirect(reverse("dashindex"))

@login_required
def dashboard_view(request):
    if request.method == "GET":
        landing = Landing_Logs.objects.all()
        application = application_Logs.objects.all()
        unique = unique_Logs.objects.all()
        access = EarlyAccess.objects.all()
        return render(request, "dashboard/dashboard.html", {
            "landing": len(landing),
            "application": len(application),
            "unique": len(unique),
            "access": len(access)
        })
@login_required
def conversions(request):
    if request.method == "GET":
        early = EarlyAccess.objects.all()
        return render(request, "dashboard/conversions.html", {
            "early": early
        })