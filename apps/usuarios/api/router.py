from django.urls import path
from .ViewUsuarios import UserViewSet, UserView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .ViewUsuarios import CustomTokenObtainPairView, DetallesUsuarioByEmailView
from apps.usuarios.views import generate_pdf

urlpatterns = [
    path('usuarios/', UserViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('usuarios/<int:pk>/', UserViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('usuarios/email/<email>/', DetallesUsuarioByEmailView.as_view()),
    
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/me', UserView.as_view()),
    path('usuarios/generate-pdf/', generate_pdf, name='generate_pdf'),

]