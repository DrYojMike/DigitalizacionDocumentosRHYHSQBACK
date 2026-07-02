from django.contrib.auth.hashers import check_password


class PasswordService:


    @staticmethod
    def verify(raw_password, stored_password):

        # mientras está en texto plano
        if raw_password == stored_password:
            return True


        # futuro: contraseña cifrada Django
        try:
            return check_password(
                raw_password,
                stored_password
            )
        except:
            return False