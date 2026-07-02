from users.models import Empleados


class EmployeRepository:


    @staticmethod
    def find_by_documento(documento):

        return (
            Empleados.objects
            .filter(documentoEmpleado=documento)
            .first()
        )