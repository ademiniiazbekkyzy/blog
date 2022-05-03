from django.urls import path, include
from rest_framework.routers import DefaultRouter
from post.views import *

router = DefaultRouter()
router.register('', PostViewSet)

urlpatterns = [
    path('categories/', CategoryListCreateView.as_view()),
    path('category/<str:slug>/', CategoryRetrieveDeleteUpdateView.as_view()),
    path('comments/', CommentsListView.as_view()),
    path('comment/<str:product>/', CommentsRetrieveDeleteUpdateView.as_view()),
    path('favorites/', FavoriteListView.as_view()),
    path('', include(router.urls)),
]
