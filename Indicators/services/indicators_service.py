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

    @staticmethod
    def getIndicadorEvaluation():

        evaluation_general = IndicatorsRepository.getIndicatorEvaluationGeneral()
        evaluation_type1 = IndicatorsRepository.getIndicatorEvaluationType1()
        evaluation_type2 = IndicatorsRepository.getIndicatorEvaluationType2()

        general = evaluation_general[0] if evaluation_general else []
        tipo1 = evaluation_type1[0] if evaluation_type1 else []
        tipo2 = evaluation_type2[0] if evaluation_type2 else []

        return {
            "general": {
                "eficienciaEnElTrabajo": general[0],
                "conocimientosTecnicos": general[1],
                "destrezaEnLaRealizacionDelTrabajo": general[2],
                "cumplimientoDeNormasYProcedimientos": general[3],
                "compromisoOrganizacional": general[4],
                "supervision": general[5],
                "tomaDeDecisiones": general[6],
                "trabajoEnEquipo": general[7],
                "direccionamientoEstrategico": general[8],
                "participacionYCapacitacion": general[9],
                "desarrolloDeLasActividades": general[10],
                "relacionesInterpersonales": general[11],
                "creatividadEIniciativa": general[12],
            },

            "tipo1": {
                "eficienciaEnElTrabajo": tipo1[0],
                "conocimientosTecnicos": tipo1[1],
                "destrezaEnLaRealizacionDelTrabajo": tipo1[2],
                "cumplimientoDeNormasYProcedimientos": tipo1[3],
                "compromisoOrganizacional": tipo1[4],
                "supervision": tipo1[5],
                "tomaDeDecisiones": tipo1[6],
                "trabajoEnEquipo": tipo1[7],
                "direccionamientoEstrategico": tipo1[8],
                "participacionYCapacitacion": tipo1[9],
                "desarrolloDeLasActividades": tipo1[10],
            },

            "tipo2": {
                "eficienciaEnElTrabajo": tipo2[0],
                "conocimientosTecnicos": tipo2[1],
                "destrezaEnLaRealizacionDelTrabajo": tipo2[2],
                "cumplimientoDeNormasYProcedimientos": tipo2[3],
                "compromisoOrganizacional": tipo2[4],
                "direccionamientoEstrategico": tipo2[5],
                "participacionYCapacitacion": tipo2[6],
                "desarrolloDeLasActividades": tipo2[7],
                "relacionesInterpersonales": tipo2[8],
                "creatividadEIniciativa": tipo2[9],
            },
        }