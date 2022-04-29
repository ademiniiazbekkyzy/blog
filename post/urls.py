from django.urls import path, include
from rest_framework.routers import DefaultRouter
from post.views import *

router = DefaultRouter()
router.register('', ProductViewSet)

urlpatterns = [
    path('category/', CategoryListCreateView.as_view()),
    path('category/<str:slug>/', CategoryRetriveDeleteUpdateView.as_view()),
    path('', include(router.urls)),
]
