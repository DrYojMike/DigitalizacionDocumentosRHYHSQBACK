from users.services.admin_service import AdminService
from users.services.employee_service import EmployeeService


class UserService:

    @staticmethod
    def get_profile(user):

        if user.role == "ADMIN":
            return AdminService.get_profile(user.nomUsuario)

        if user.role == "EMPLEADO":
            return EmployeeService.get_profile(user.documentoEmpleado)

        raise ValueError("Rol inválido")