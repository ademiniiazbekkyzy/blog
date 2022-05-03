from django.urls import path, include

from account.views import RegisterApiView, LoginApiView, LogoutView, ChangePasswordView, ActivationView

urlpatterns = [
    path('register/', RegisterApiView.as_view()),
    path('activate/<uuid:activation_code>/', ActivationView.as_view()),
    path('login/', LoginApiView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('change-password/', ChangePasswordView.as_view()),
    path('password_reset/', include('django_rest_passwordreset.urls'))
]
