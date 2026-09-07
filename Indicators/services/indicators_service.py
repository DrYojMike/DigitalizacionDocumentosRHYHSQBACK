from Indicators.repositories.indicators_repository import IndicatorsRepository

class IndicatorsService():
    @staticmethod
    def getStaffTurnover():
        data = IndicatorsRepository.getStaffTurnover()
        
        if not data:
            return None
        response = []
        
        for row in data:
            mes = row[1]
            if mes not in response:
                response.append({
                    "Anio": row[0],
                    "Mes": row[1],
                    "EmpleadoInicio": row[2],
                    "Ingresos": row[3],
                    "Retiros": row[4],
                    "EmpleadosFinal": row[5],
                    "PromedioEmpleados": row[6],
                    "PorcetajeRotacion": row[7]
                })
            
        return response

    @staticmethod
    def getPerformanceEvaluation():
        data = IndicatorsRepository.getPerformanceEvaluation()

        if not data:
            return None
        info = {}

        for row in data:
            idArea = row[0]
            # AREA
            if idArea not in info:
                info[idArea] = {
                    "id": idArea,
                    "nombre": row[1],
                    "cumplimiento": row[9],
                    "competencias": {}
                }
                
            idCompetencia = row[2]
            # COMPETENCIA
            if idCompetencia not in info[idArea]["competencias"]:
                info[idArea]["competencias"][idCompetencia] = {
                    "id": idCompetencia,
                    "nombre": row[3],
                    "descripcion": row[4],
                    "cumplimiento": row[8],
                    "indicadores": {}
                }

            idIndicador = row[5]
            # INDICADOR
            if idIndicador not in info[idArea]["competencias"][idCompetencia]["indicadores"]:
                info[idArea]["competencias"][idCompetencia]["indicadores"][idIndicador] = {
                    "id": idIndicador,
                    "nombre": row[6],
                    "cumplimiento": row[7]
                }

        # Convertir diccionarios a listas para la respuesta JSON
        response = []

        for area in info.values():

            area["competencias"] = list(area["competencias"].values())

            for competencia in area["competencias"]:
                competencia["indicadores"] = list(
                    competencia["indicadores"].values()
                )

            response.append(area)

        return response
