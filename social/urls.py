from rest_framework.routers import DefaultRouter
from .views import PostViewSet
from django.urls import path
from .views import ProfileDetailView



router = DefaultRouter()
router.register(r"posts", PostViewSet, basename="post")

urlpatterns = router.urls + [
    path("profiles/<str:username>/", ProfileDetailView.as_view()),
]


