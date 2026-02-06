from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def feed_view(request):
    return render(request, "frontend/feed.html")

def login_view(request):
    return render(request, "frontend/login.html")

def profile_view(request, username):
    return render(request, "frontend/profile.html", {"username": username})

def home(request):
    return render(request, "frontend/home.html")