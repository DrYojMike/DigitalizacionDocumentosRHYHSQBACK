from users.repositories.employe_repositories import EmployeRepository

from EvaluacionDesempeno.repositories.AutoEvaluacion_Empleado_repository import (
    AutoEvaluacionEmpleadoReposity
)

from EvaluacionDesempeno.repositories.Evaluar_Empleado_Jefe_repository import (
    EvaluacionEmpleadoJefeRepository
)


class EmployeeService:

    @staticmethod
    def build_profile(empleado):

        return {

            "id": empleado.idEmpleado,
            "documento": empleado.documentoEmpleado,
            "name": empleado.nombreEmpleado,
            "role": "EMPLEADO",

            "permissions": {

                "evaluacion":
                    AutoEvaluacionEmpleadoReposity
                    .has_evaluation_this_year(
                        empleado.documentoEmpleado
                    ),

                "empleadosCargo":
                    EvaluacionEmpleadoJefeRepository
                    .has_employ_whit_evaluations(
                        empleado.documentoEmpleado
                    ),

                "tipoEvaluacion":
                    empleado.evaluacionTipo

            }

        }

    @staticmethod
    def get_profile(documento):

        empleado = EmployeRepository.find_by_documento(documento)

        if not empleado:
            raise ValueError("Empleado no encontrado")

        return EmployeeService.build_profile(empleado)