from EvaluacionDesempeno.repositories.Evaluar_Empleado_Jefe_repository import EvaluacionEmpleadoJefeRepository
from Functions.repositories.evaluacion_email_info_repository import EvaluationEmailInfoRepository
from Functions.services.email_evaluation import EvaluationEmailService

import logging
logger = logging.getLogger(__name__)

class EvaluarEmpleadoService:
    @staticmethod
    def execute(jefe):

        empleados = (
            EvaluacionEmpleadoJefeRepository.list_employes_evaluation(jefe)
        )

        return empleados
    
    @staticmethod
    def get_autoevaluacion_empleado(idEvaGen):

        rows = EvaluacionEmpleadoJefeRepository.get_evaluacio_empleado(idEvaGen)

        if not rows:
            return None

        data = {
            "idEvaluacion": rows[0][0],
            "fecha": rows[0][1],
            "idEmpleado": rows[0][10],
            "idJefe": rows[0][11],
            "areas": []
        }

        areas = {}

        for row in rows:

            idArea = row[2]
            idCompetencia = row[4]

            if idArea not in areas:

                areas[idArea] = {
                    "idArea": idArea,
                    "area": row[3],
                    "competencias": {}
                }

            competencias = areas[idArea]["competencias"]

            if idCompetencia not in competencias:

                competencias[idCompetencia] = {
                    "idCompetencia": idCompetencia,
                    "nombre": row[5],
                    "descripcion": row[6],
                    "indicadores": []
                }

            competencias[idCompetencia]["indicadores"].append({
                "idIndicador": row[7],
                "indicador": row[8],
                "nota": row[9]
            })

        resultado_areas = []

        for area in areas.values():

            area["competencias"] = list(
                area["competencias"].values()
            )

            resultado_areas.append(area)

        data["areas"] = resultado_areas

        return data

    @staticmethod
    def evaluar_empleado(data):
        respuestas = data["respuestas"]
        
        for item in respuestas:

            EvaluacionEmpleadoJefeRepository.evaluate_a_employee(
                idEva=item["idEva"],
                idJefe=item["idJefe"],
                idEmp=item["idEmp"],
                nota=item["nota"],
                idIndicador=item["idIndicador"]
            )

        if data.get("compromisos"):

            idEva = respuestas[0]["idEva"]
            idJefe = respuestas[0]["idJefe"]

            for compromiso in data["compromisos"]:

                EvaluacionEmpleadoJefeRepository.compromisos_evaluate_a_employe(
                    idEva=idEva,
                    idJefe=idJefe,
                    compromiso=compromiso
                )
        info = EvaluationEmailInfoRepository.get_employee_and_manager(respuestas[0]["idEmp"])
        if info:
            try:
                EvaluationEmailService.notify_employee(
                    employee_name=info["employee_name"],
                    employee_email=info["employee_email"],
                    manager_name=info["manager_name"]
                )
            except Exception as e:
                logger.exception(e)
        return {
            "message": "Evaluación guardada correctamente"
        }