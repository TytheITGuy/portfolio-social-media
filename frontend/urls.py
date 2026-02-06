from django.urls import path
from django.contrib.auth import views as auth_views
from .views import home, feed_view, profile_view

urlpatterns = [
    path("", home, name="home"),
    path("feed/", feed_view, name="feed"),
    path("profile/<str:username>/", profile_view, name="profile"),

    # Auth (Django built-in)
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="frontend/login.html"),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]

