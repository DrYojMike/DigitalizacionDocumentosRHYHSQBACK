from rest_framework_simplejwt.tokens import RefreshToken


class JWTService:

    @staticmethod
    def generate(user):

        refresh = RefreshToken()

        refresh["user_id"] = user["id"]
        refresh["role"] = user["role"]

        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        }