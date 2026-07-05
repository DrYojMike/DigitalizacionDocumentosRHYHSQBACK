from EvaluacionDesempeno.repositories.AutoEvaluacion_Empleado_repository import(AutoEvaluacionEmpleadoReposity)
from Functions.repositories.evaluacion_email_info_repository import EvaluationEmailInfoRepository
from Functions.services.email_evaluation import EvaluationEmailService
import logging
logger = logging.getLogger(__name__)

class AutoEvaluacionService:
    
    @staticmethod
    def get_evaluation_format(tipo):
        rows = AutoEvaluacionEmpleadoReposity.get_format(tipo)
        data = {}
        for row in rows:
            area_id = row[0]
            area_name = row[1]
            comp_id = row[2]
            comp_name = row[3]
            comp_desc = row[4]
            ind_id = row[5]
            ind_name = row[6]

            if area_id not in data:
                data[area_id] = {
                    "area": area_name,
                    "competencias": {}
                }

            if comp_id not in data[area_id]["competencias"]:
                data[area_id]["competencias"][comp_id] = {
                    "nombre": comp_name,
                    "descripcion": comp_desc,
                    "indicadores": []
                }

            data[area_id]["competencias"][comp_id]["indicadores"].append({
                "id": ind_id,
                "nombre": ind_name
            })

        result = []
        for area in data.values():
            area["competencias"] = list(
                area["competencias"].values()
            )
            result.append(area)
        return result
    
    
    @staticmethod
    def create_evaluation(data):
        documento = data["idUsuario"]
        print(documento)
        # validar año
        if AutoEvaluacionEmpleadoReposity.has_evaluation_this_year(documento):
            return {
                "message":"Ya realizó la evaluación de este año"
            }
        # crear cabecera
        id_general = (
            AutoEvaluacionEmpleadoReposity.create_evaluation()
        )
        # guardar indicadores
        empleado = data["idUsuario"]
        for item in data["respuestas"]:
            AutoEvaluacionEmpleadoReposity.create_item_evaluation(
                nota=item["nota"],
                id_general=id_general,
                empleado=empleado,
                indicador=item["indicador_id"]
            )
        
        info = EvaluationEmailInfoRepository.get_employee_and_manager(documento)
        if info:
            try:
                EvaluationEmailService.notify_AutoEvaluation(
                    employee_name=info["employee_name"],
                    employee_email=info["employee_email"]
                )
            except Exception as e:
                logger.exception(e)
        return {
            "message":"Evaluación creada correctamente",
            "id":id_general
        }
    
    
    @staticmethod
    def get_evaluation_info(idEvaluacion):
        rows = AutoEvaluacionEmpleadoReposity.evaluacion_info(idEvaluacion)

        if not rows:
            return None

        data = {
            "usuario": rows[0][0],
            "jefe": rows[0][1],
            "fecha": rows[0][2],
            "areas": [],
            "compromisos": []
        }

        areas = {}
        compromisos = {}

        for row in rows:

            idArea = row[3]

            if idArea not in areas:
                areas[idArea] = {
                    "idArea": idArea,
                    "area": row[4],
                    "competencias": {}
                }

            competencias = areas[idArea]["competencias"]
            idCompetencia = row[5]

            if idCompetencia not in competencias:
                competencias[idCompetencia] = {
                    "idCompetencia": idCompetencia,
                    "nombre": row[6],
                    "descripcion": row[7],
                    "indicadores": [],
                    "_indicadores": set()  # Evita duplicados
                }

            competencia = competencias[idCompetencia]

            idIndicador = row[8]

            if idIndicador not in competencia["_indicadores"]:
                competencia["indicadores"].append({
                    "idIndicador": idIndicador,
                    "indicador": row[9],
                    "nota": row[10],
                    "notaJefe": row[11]
                })

                competencia["_indicadores"].add(idIndicador)

            idCompromiso = row[12]

            if (
                idCompromiso is not None
                and idCompromiso not in compromisos
            ):
                compromisos[idCompromiso] = {
                    "idCompromiso": idCompromiso,
                    "compromiso": row[13]
                }

        # Convertir competencias a lista y eliminar el campo auxiliar
        for area in areas.values():

            for competencia in area["competencias"].values():
                competencia.pop("_indicadores", None)

            area["competencias"] = list(area["competencias"].values())

        data["areas"] = list(areas.values())
        data["compromisos"] = list(compromisos.values())

        return data


    @staticmethod
    def list_evaluations(idUsuario):
        evaluaciones = AutoEvaluacionEmpleadoReposity.get_my_evaluations(idUsuario)
        return evaluaciones