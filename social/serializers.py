from rest_framework import serializers
from .models import Post,  Profile


class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source="author.username")
    like_count = serializers.IntegerField(source="likes.count", read_only=True)
    liked_by_me = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ["id", "author", "author_username", "content", "created_at", "like_count", "liked_by_me"]
        read_only_fields = ["id", "author", "author_username", "created_at", "like_count", "liked_by_me"]

    def get_liked_by_me(self, obj):
        request = self.context.get("request")
        if request and request.user and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False
    
    
class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source="user.username")
    date_joined = serializers.ReadOnlyField(source="user.date_joined")
    post_count = serializers.IntegerField(source="user.posts.count", read_only = True)
    likes_give = serializers.IntegerField(source="user.likes.count", read_only = True)
    
    
    class Meta:
        model = Profile
        fields = [
            "username",
            "bio",
            "avatar_url",
            "date_joined",
            "post_count",
            "likes_given",
        ]
        read_only_fields = [
            "username",
            "date_joined",
            "post_count",
            "likes_given",
        ]