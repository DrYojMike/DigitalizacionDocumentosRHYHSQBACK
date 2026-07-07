from EvaluacionDesempeno.repositories.AdminEvaluacion_repositoy import EvaluationAdminRepository

class EvaluationAdminService:
    @staticmethod
    def getIndicadorIndGestion():
        indicadorGestion = EvaluationAdminRepository.indicadorIndicadoresGestion()

        if not indicadorGestion:
            return None
        resultado = {}
        
        for row in indicadorGestion:
            anio = row[0]
            if anio not in resultado:
                resultado[anio] = {
                    "Año": anio,
                    "indicadores": {}
                }
            indicadores = resultado[anio]["indicadores"]
            idIndicador = row[1]
            if idIndicador not in indicadores:
                indicadores[idIndicador] = {
                    "id": idIndicador,
                    "indicador": row[2],
                    "cantEvaluaciones": row[3],
                    "notMaxima": row[4],
                    "notIndicador": row[5],
                    "promedio":row[6]
                }
            else:
                indicadores[idIndicador]["cantEvaluaciones"] += row[3]
                indicadores[idIndicador]["notMaxima"] += row[4]
                indicadores[idIndicador]["notIndicador"] += row[5]
                indicadores[idIndicador]["promedio"] += row[5]

        data = []

        for anio in resultado.values():
            for indicador in anio["indicadores"].values():
                indicador["promedio"] = (
                    100 * indicador["notIndicador"] / indicador["notMaxima"] 
                    if indicador["notMaxima"] > 0 else 0
                )

            anio["indicadores"] = list(anio["indicadores"].values())
            data.append(anio)

        return data
    
    def getIndicadorCompetencia():
        comeptencia = EvaluationAdminRepository.indicadorCompetencia()
        
        if not comeptencia:
            return None
        resultado = {}
    
        for row in comeptencia:
            anio = row[0]
            if not anio in resultado:
                resultado[anio]={
                    "Anio": anio,
                    "competencias":{}
                }
            
            competencias = resultado[anio]["competencias"]
            idCompetencia = row[1]
            if not idCompetencia in competencias:
                competencias[idCompetencia]={
                    "id":idCompetencia,
                    "competencia":row[2],
                    "descripcion":row[3],
                    "cantEvaluaciones":row[4],
                    "notMaxima":row[5],
                    "notCompetencia":row[6],
                    "promedio":row[7]
                }
            else:
                competencias[idCompetencia]["cantEvaluaciones"]+=row[4]
                competencias[idCompetencia]["notMaxima"]+=row[5]
                competencias[idCompetencia]["notCompetencia"]+=row[6]
            
        data = []
        for anio in resultado.values():
            for competencias in anio["competencias"].values():
                competencias["promedio"] = (
                    100 * competencias["notCompetencia"] / competencias["notMaxima"]
                    if competencias["notMaxima"] > 0 else 0
                )

            anio["competencias"] = list(anio["competencias"].values())
            data.append(anio)
        
        return data

    