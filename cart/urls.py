from rest_framework.routers import DefaultRouter

from cart.views import CartViewSet

router = DefaultRouter()
router.register('', CartViewSet)

urlpatterns = []
urlpatterns.extend(router.urls)
