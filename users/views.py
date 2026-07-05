from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.serializers import LoginSerializer
from users.services.auth_service import AuthServices
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RefreshSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from users.services.user_service import UserService
from users.authentication.jwt import JWTService
from users.authentication.custom import CustomJWTAuthentication, IsCustomAuthenticated
# Create your views here.
class LoginView(APIView):
    authentication_classes=[]
    permission_classes=[]
    
    def post(self,request):
        serializer = LoginSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        try:
            user = AuthServices.login(
                serializer.validated_data["username"],
                serializer.validated_data["password"]
            )
            
            tokens = JWTService.generate(user)

            return Response({
                "user":user,
                "tokens":tokens
            })

        except ValueError as error:
            print(str(error))
            return Response(
                {
                    "message": "Credenciales Invalidas"
                },
                status=status.HTTP_401_UNAUTHORIZED
            )


class RefreshTokenView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsCustomAuthenticated]
    def post(self, request):
        serializer = RefreshSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            refresh = RefreshToken(serializer.validated_data["refresh"])

            return Response(
                {
                    "access":str(refresh.access_token)
                }
            )
        except Exception:
            return Response(
                {
                    "message":"Refresh token inválido"
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
            

class MeView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsCustomAuthenticated]
    def get(self, request):
        return Response(
        UserService.get_profile(request.user
        )
    )