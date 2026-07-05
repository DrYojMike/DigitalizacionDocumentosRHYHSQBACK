from users.repositories.users_repositories import AdminRepository
from users.repositories.employe_repositories import EmployeRepository

from users.services.password_service import PasswordService
from users.services.admin_service import AdminService
from users.services.employee_service import EmployeeService


class AuthServices:

    @staticmethod
    def login(username, password):

        usuario = AdminRepository.find_by_username(username)

        if usuario:

            if PasswordService.verify(password, usuario.clave):

                return AdminService.build_profile(usuario)

        empleado = EmployeRepository.find_by_documento(username)

        if empleado:

            if PasswordService.verify(password, empleado.documentoEmpleado):

                return EmployeeService.build_profile(empleado)

        raise ValueError({"message": "Credenciales inválidas"})