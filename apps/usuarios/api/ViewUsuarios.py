from rest_framework import viewsets, status
from ..api.UsuarioSeralizers import UsuarioSerializer, UserSerializerToken
from rest_framework_simplejwt.views import TokenObtainPairView
from ..api.UsuarioSeralizers import CustomTokenObtainPairSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from ..models import Usuario

from django.utils import timezone
from django.contrib.auth.tokens import default_token_generator
from ..models import PasswordResetToken, Usuario

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
    
class GenerateTokenView(APIView):
    def post(self, request):
        email = request.data.get('email')
        try:
            usuario = Usuario.objects.get(email=email)
        except Usuario.DoesNotExist:
            return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        # Verificar si el usuario ya tiene un token activo
        if PasswordResetToken.objects.filter(user=usuario, used=False).exists():
            return Response({'error': 'Ya se ha solicitado un restablecimiento de contraseña'}, status=status.HTTP_400_BAD_REQUEST)

        # Generar un nuevo token
        token = default_token_generator.make_token(usuario)
        PasswordResetToken.objects.create(user=usuario, token=token)

        # Devolver el token generado
        return Response({'token': token}, status=status.HTTP_200_OK)

class ResetPasswordView(APIView):
    def post(self, request):
        token = request.data.get('token')
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')

        # Verificar si las contraseñas coinciden
        if new_password != confirm_password:
            return Response({'error': 'Las contraseñas no coinciden'}, status=status.HTTP_400_BAD_REQUEST)

        # Verificar si el token es válido
        try:
            token_obj = PasswordResetToken.objects.get(token=token, used=False, created_at__gte=timezone.now()-timezone.timedelta(minutes=30))
        except PasswordResetToken.DoesNotExist:
            return Response({'error': 'Token inválido o expirado'}, status=status.HTTP_400_BAD_REQUEST)

        # Cambiar la contraseña del usuario
        usuario = token_obj.user
        usuario.set_password(new_password)
        usuario.save()

        # Marcar el token como utilizado
        token_obj.used = True
        token_obj.save()

        return Response({'message': 'Contraseña restablecida correctamente'}, status=status.HTTP_200_OK)
