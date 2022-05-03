# Create your views here.
from datetime import timedelta

from django.db.models import Q
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from requests import request
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import *
from rest_framework.mixins import *
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from post.filters import PostFilter
from post.models import Post, Rating, Category, Like, Favorite, Comments
from post.permissions import IsAuthor
from post.serializers import PostSerializer, RatingSerializers, CategorySerializers, FavoriteSerializers, \
    CommentsSerializers


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 1000000


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = LargeResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = PostFilter
    ordering_fields = ['id', 'price']
    search_fields = ['name', 'description']

    @action(methods=['GET'], detail=False)
    def search(self, request, pk=None):
        q = request.query_params.get('q')
        queryset = self.get_queryset()
        queryset = queryset.filter(Q(name__icontains=q) | Q(description__icontains=q))
        serializer = PostSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permissions = []
        elif self.action == 'rating':
            permissions = [IsAuthenticated]
        else:
            permissions = [IsAuthenticated]
        return [permission() for permission in permissions]

    def get_queryset(self):
        queryset = super().get_queryset()
        days_count = int(self.request.query_params.get('day', 0))
        if days_count > 0:
            start_date = timezone.now() - timedelta(days=days_count)
            queryset = queryset.filter(created_at__gte=start_date)
        return queryset



    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(methods=['POST'], detail=True)
    def rating(self, request, pk): # http://localhost:8000/api/v1/product/id_product/rating/
        serializer = RatingSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            obj = Rating.objects.get(product=self.get_object(),
                                     owner=request.user)
            obj.rating = request.data['rating']
        except Rating.DoesNotExist:
            obj = Rating(owner=request.user,
                         product=self.get_object(),
                         rating=request.data['rating']
                        )
            obj.save()
        return Response(request.data,
                        status=status.HTTP_201_CREATED)

    @action(methods=['POST'], detail=True)
    def like(self, request, *args, **kwargs):
        product = self.get_object()
        like_obj, _ = Like.objects.get_or_create(product=product, owner=request.user)
        like_obj.like = not like_obj.like
        like_obj.save()
        status = 'liked'
        if not like_obj.like:
            status = 'unlike'
        return Response({'status': status})

    @action(methods=['POST'], detail=True)
    def favorite(self, request, *args, **kwargs):
        # queryset = Post.objects.filter(owner=request.user)
        product = self.get_object()
        favorite_obj, _ = Favorite.objects.get_or_create(product=product, owner=request.user)
        favorite_obj.favorite = not favorite_obj.favorite
        favorite_obj.save()
        status = 'Added to favorites'
        if not favorite_obj.favorite:
            status = 'Removed from favorites'
        return Response({'status': status})

    @action(methods=['POST'], detail=True)
    def comment(self, request, pk):  # http://localhost:8000/api/v1/product/id_product/comment/
        serializer = CommentsSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            obj = Comments.objects.get(product=self.get_object(),
                                     owner=request.user)
            obj.comments = request.data['comments']
        except Comments.DoesNotExist:
            obj = Comments(owner=request.user,
                         product=self.get_object(),
                         comments=request.data['comments']
                         )
            obj.save()
        return Response(request.data,
                        status=status.HTTP_201_CREATED)


class CategoryListCreateView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers
    permission_classes = [IsAuthenticated]


class FavoriteListView(ListAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializers
    permission_classes = [IsAuthenticated, IsAuthor]

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        queryset = queryset.filter(owner=user)
        return queryset


class CategoryRetrieveDeleteUpdateView(RetrieveUpdateDestroyAPIView):
    lookup_field = 'slug'
    queryset = Category.objects.all()
    serializer_class = CategorySerializers
    permission_classes = [IsAuthenticated]


class CommentsRetrieveDeleteUpdateView(RetrieveUpdateDestroyAPIView):
    lookup_field = 'comment'
    queryset = Comments.objects.all()
    serializer_class = CategorySerializers
    permission_classes = [IsAuthenticated]


class CommentsListView(ListAPIView):
    queryset = Comments.objects.all()
    serializer_class = FavoriteSerializers
    permission_classes = [IsAuthenticated]

