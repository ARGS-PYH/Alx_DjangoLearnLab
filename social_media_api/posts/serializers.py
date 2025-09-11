from django.conf import settings
from rest_framework import serializers
from .models import Post, Comment
from django.contrib.auth import get_user_model

User = get_user_model()

class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source="author.username", read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "post", "author", "author_username", "content", "created_at", "updated_at"]
        read_only_fields = ["id", "author", "author_username", "created_at", "updated_at"]

class PostListSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source="author.username", read_only=True)
    comment_count = serializers.IntegerField(source="comments.count", read_only=True)

    class Meta:
        model = Post
        fields = ["id", "title", "author", "author_username", "comment_count", "created_at", "updated_at"]

class PostDetailSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source="author.username", read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ["id", "title", "content", "author", "author_username", "comments", "created_at", "updated_at"]
        read_only_fields = ["id", "author", "author_username", "comments", "created_at", "updated_at"]
