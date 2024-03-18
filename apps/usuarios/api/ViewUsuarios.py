from rest_framework import viewsets
from ..api.UsuarioSeralizers import UsuarioSerializer, UserSerializerToken
from rest_framework_simplejwt.views import TokenObtainPairView
from ..api.UsuarioSeralizers import CustomTokenObtainPairSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from ..models import Usuario

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UsuarioSerializer
    queryset =  UsuarioSerializer.Meta.model.objects.all()
    # # permission_classes = [IsAuthenticated]

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serealizer = UserSerializerToken(request.user)
        return Response(serealizer.data)
    

class DetallesUsuarioByEmailView(generics.ListAPIView):
    serializer_class = UsuarioSerializer  # Asegúrate de importar el serializador adecuado
    queryset = Usuario.objects.all()  # Define el queryset inicial

    def get_queryset(self):
        email = self.kwargs['email']
        return Usuario.objects.filter(email=email)