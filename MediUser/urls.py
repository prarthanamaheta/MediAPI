from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView, TokenVerifyView,
)
from MediUser.views import MediUserRegister, MediUserLogin

urlpatterns = [
    path('MediUser/register', MediUserRegister.as_view()),
    path('MediUser/login',MediUserLogin.as_view()),
    path('MediUser/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('MediUser/token_refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('MediUser/token_verify/', TokenVerifyView.as_view(), name='token_verify'),
]
