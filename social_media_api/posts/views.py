from rest_framework import viewsets, permissions, filters
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404

from .models import Post, Comment
from .serializers import PostListSerializer, PostDetailSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly

# Pagination
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.select_related("author").prefetch_related("comments").all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["author__username", "created_at"]   
    search_fields = ["title", "content", "author__username"]
    ordering_fields = ["created_at", "title"]
    pagination_class = StandardResultsSetPagination

    def get_serializer_class(self):
        if self.action in ["list"]:
            return PostListSerializer
        return PostDetailSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.select_related("author", "post").all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ["post", "author__username"]
    search_fields = ["content", "author__username"]
    ordering_fields = ["created_at"]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
