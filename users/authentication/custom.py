from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

from users.models import Usuarios, Empleados
from rest_framework.permissions import BasePermission

class CustomJWTAuthentication(JWTAuthentication):

    def get_user(self, validated_token):

        user_id = validated_token.get("user_id")
        role = validated_token.get("role")

        if not user_id:
            raise AuthenticationFailed("Token inválido")

        try:

            if role == "ADMIN":

                usuario = Usuarios.objects.get(idUsuario=user_id)

                # Agregamos el rol al objeto
                usuario.role = role

                return usuario

            if role == "EMPLEADO":

                empleado = Empleados.objects.get(idEmpleado=user_id)

                # Agregamos el rol al objeto
                empleado.role = role

                return empleado

        except Exception:
            raise AuthenticationFailed("Usuario no encontrado")

        raise AuthenticationFailed("Rol inválido")

class IsCustomAuthenticated(BasePermission):

    def has_permission(self, request, view):

        return hasattr(request.user, "role")