from rest_framework import serializers

from ..models import *
from apps.rol.api.RoleSeralizers import RolSeralizers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers




class UsuarioSerializer(serializers.ModelSerializer):
    rol = RolSeralizers(source='id_rol_fk', read_only=True)
    class Meta:
        model = Usuario
        fields = '__all__'  # Incluir todos los campos del modelo
        
    def create(self, validated_data):
        groups_data = validated_data.pop('groups', None)
        permissions_data = validated_data.pop('user_permissions', None)
        password = validated_data.pop('password', None)

        user = self.Meta.model(**validated_data)
        if password is not None:
            user.set_password(password)
        user.save()

        if groups_data is not None:
            user.groups.set(groups_data)
        
        if permissions_data is not None:
            user.user_permissions.set(permissions_data)
        
        return user

    def update(self, instance, validated_data):
        groups_data = validated_data.pop('groups', None)
        permissions_data = validated_data.pop('user_permissions', None)
        password = validated_data.pop('password', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password is not None:
            instance.set_password(password)
        instance.save()

        if groups_data is not None:
            instance.groups.set(groups_data)
        
        if permissions_data is not None:
            instance.user_permissions.set(permissions_data)

        return instance


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        # Renombrar la clave 'access' a 'token'
        data['token'] = data.pop('access')
        return data

class UserSerializerToken(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'  # Incluir todos los campos del modelo