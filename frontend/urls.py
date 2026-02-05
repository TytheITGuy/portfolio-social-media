from django.urls import path
from . import views

urlpatterns = [
    path("", views.feed_view, name="feed"),
    path("login/", views.login_view, name="login"),
    path("profile/<str:username>/", views.profile_view, name="profile"),
]