from users.models import Usuarios


class AdminRepository:


    @staticmethod
    def find_by_username(username):

        return (
            Usuarios.objects
            .filter(nomUsuario=username)
            .first()
        )