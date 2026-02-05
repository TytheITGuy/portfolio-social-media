from django.shortcuts import render

# Create your views here.
def feed_view(request):
    return render(request, "frontend/feed.html")

def login_view(request):
    return render(request, "frontend/login.html")

def profile_view(request, username):
    return render(request, "frontend/profile.html", {"username": username})

