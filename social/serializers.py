from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Post, Profile

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source="author.username")
    like_count = serializers.IntegerField(source="likes.count", read_only=True)
    liked_by_me = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "id",
            "author",
            "author_username",
            "content",
            "created_at",
            "like_count",
            "liked_by_me",
        ]
        read_only_fields = [
            "id",
            "author",
            "author_username",
            "created_at",
            "like_count",
            "liked_by_me",
        ]

    def get_liked_by_me(self, obj):
        request = self.context.get("request")
        if request and request.user and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source="user.username")
    date_joined = serializers.ReadOnlyField(source="user.date_joined")

    post_count = serializers.SerializerMethodField()
    likes_given = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ["username", "bio", "avatar_url", "date_joined", "post_count", "likes_given"]
        read_only_fields = ["username", "date_joined", "post_count", "likes_given"]

    def get_post_count(self, obj):
        return obj.user.post_set.count()

    def get_likes_given(self, obj):
        return obj.user.like_set.count()


class MeSerializer(serializers.ModelSerializer):
    bio = serializers.ReadOnlyField(source="profile.bio")
    avatar_url = serializers.ReadOnlyField(source="profile.avatar_url")

    class Meta:
        model = User
        fields = ["id", "username", "bio", "avatar_url"]
        read_only_fields = fields

