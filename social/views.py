from django.db import IntegrityError
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import Like, Post
from .permissions import IsOwnerOrReadOnly
from .serializers import PostSerializer

from django.contrib.auth.models import User
from .models import Profile
from .serializers import ProfileSerializer

from rest_framework.generics import RetrieveAPIView


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by("-created_at")
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        post = self.get_object()
        try:
            Like.objects.create(user=request.user, post=post)
            return Response({"detail": "Liked"}, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({"detail": "Already liked"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["delete"], permission_classes=[IsAuthenticated])
    def unlike(self, request, pk=None):
        post = self.get_object()
        deleted, _ = Like.objects.filter(user=request.user, post=post).delete()
        if deleted:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": "Not liked"}, status=status.HTTP_200_OK)


class ProfileDetailView(RetrieveAPIView):
    serialzer_class = ProfileSerializer
    lookup_field = "user_username"
    lookup_url_kwarg = "username"
    
    def get_queryset(self):
        return Profile.objects.select_related("user")



    