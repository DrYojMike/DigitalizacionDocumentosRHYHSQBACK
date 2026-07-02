from users.repositories.users_repositories import AdminRepository


class AdminService:

    @staticmethod
    def build_profile(usuario):

        return {

            "id": usuario.idUsuario,
            "username": usuario.nomUsuario,
            "name": f"{usuario.nomUsu} {usuario.apeUsu}",
            "role": "ADMIN",

            "permissions": {

                # Ejemplo
                "usuarios": True,
                "evaluaciones": True,
                "reportes": True

            }

        }

    @staticmethod
    def get_profile(username):

        usuario = AdminRepository.find_by_username(username)

        if not usuario:
            raise ValueError("Administrador no encontrado")

        return AdminService.build_profile(usuario)