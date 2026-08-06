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
                    "notMaxEvaluacion": row[5],
                    "promedio":row[6]
                }
            else:
                indicadores[idIndicador]["cantEvaluaciones"] += row[3]
                indicadores[idIndicador]["notMaxima"] += row[4]
                indicadores[idIndicador]["notMaxEvaluacion"] += row[5]

        data = []

        for anio in resultado.values():
            for indicador in anio["indicadores"].values():
                indicador["promedio"] = (
                    100 * indicador["notMaxEvaluacion"] / indicador["notMaxima"] 
                    if indicador["notMaxima"] > 0 else 0
                )

            anio["indicadores"] = list(anio["indicadores"].values())
            data.append(anio)

        return data
    
    @staticmethod
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
                    "notMaxEvaluacion":row[6],
                    "promedio":row[7]
                }
            else:
                competencias[idCompetencia]["cantEvaluaciones"]+=row[4]
                competencias[idCompetencia]["notMaxima"]+=row[5]
                competencias[idCompetencia]["notMaxEvaluacion"]+=row[6]
            
        data = []
        for anio in resultado.values():
            for competencias in anio["competencias"].values():
                competencias["promedio"] = (
                    100 * competencias["notMaxEvaluacion"] / competencias["notMaxima"]
                    if competencias["notMaxima"] > 0 else 0
                )

            anio["competencias"] = list(anio["competencias"].values())
            data.append(anio)
        
        return data

    @staticmethod
    def getindicadorArea():
        areas  =  EvaluationAdminRepository.indicadorArea()
        if not areas:
            return None
        resultado = {}
        for row in areas:
            anio = row[0]
            if not anio in resultado:
                resultado[anio]={
                    "anio": anio,
                    "areas":{}
                }
            
            idArea = row[1]
            areas = resultado[anio]["areas"]
            if not idArea in areas:
                areas[idArea]={
                    "id": idArea,
                    "Area":row[2],
                    "cantEvaluaciones":row[3],
                    "notMaxima":row[4],
                    "notMaxEvaluacion":row[5],
                    "promedio":row[6]
                }
            else:
                areas[idArea]["cantEvaluaciones"] += row[3]
                areas[idArea]["notMaxima"] += row[4]
                areas[idArea]["notMaxEvaluacion"] += row[5]
        
        data = []
        for anio in resultado.values():
            for areas in anio["areas"].values():
                areas["promedio"] = (
                    100 * areas["notMaxEvaluacion"] / areas["notMaxima"]
                    if areas["notMaxima"] > 0 else 0
                )

            anio["areas"] = list(anio["areas"].values())
            data.append(anio)
        
        return data

    @staticmethod
    def getListEvaluationEmpleye(userDocumento):
        evaluaciones = EvaluationAdminRepository.EvaluationEmployeList(userDocumento)
        if not evaluaciones:
            return []
        
        resultado = []
        
        for row in evaluaciones:
            resultado.append({
                "idEvaluacion": row[0],
                "fechaEvaluacion": row[1],
                "idEmpleado": row[2],
                "nombreEmpleado": row[3],
                "documentoEmpleado": row[4],
                "nombreJefe": row[5],
                "documentoJefe": row[6],
                "socializado": row[7],
                "SocializadoPor": row[8],
            })
        
        return resultado
    
    @staticmethod
    def getSocializacionEvaluacion(idEvaluacion):
        filas = EvaluationAdminRepository.socializarEmployeEvaluation(idEvaluacion)
        if not filas:
            return {}

        primera = filas[0]

        resultado = {
            "idEvaluacion": primera[0],
            "fechaEvaluacion": primera[1],
            "FechaSocializacion": primera[24],
            "idEmpleado": primera[2],
            "nomEmpleado": primera[3],
            "docEmpleado": primera[4],
            "cargo":primera[5],
            "nomJefe": primera[7],
            "docJefe": primera[6],
            "cargoJefe":primera[26],
            "idJefe":primera[25],
            "Indicadores":[],
            "socializacion": {},
            "compromisosJefes":[]
        }

        resultado["Indicadores"] = [
            {
                "nomber":"Compromiso",
                "nota": primera[8]
            },
            {
                "nomber":"Conocimiento",
                "nota": primera[9]
            },
            {
                "nomber":"Organización",
                "nota": primera[10]
            },
            {
                "nomber":"Normas",
                "nota": primera[11]
            },
            {
                "nombre": "Liderazgo",
                "nota": primera[12]
            },
            {
                "nombre": "Comunicación",
                "nota": primera[13]
            },
            {
                "nombre": "Respeto",
                "nota": primera[14]
            },
            {
                "nombre": "Innovación",
                "nota": primera[15]
            },
            {
                "nombre": "HSEQ",
                "nota": primera[16]
            },
            {
                "nombre": "Gestión Humana",
                "nota": primera[17]
            }
        ]
        socializacion = None
        for row in filas:
            if row[17] is None:
                continue
            if socializacion is None:
                socializacion = {
                    "idSocializacion": row[18],
                    "socializador": row[19],
                    "compromisos": []
                }
            if row[19] is not None:
                socializacion["compromisos"].append({
                    "idCompromiso": row[20],
                    "descripcion": row[21]
                })
        resultado["socializacion"] = socializacion

        compromisosJefes = resultado["compromisosJefes"]

        for row in filas:
            if row[22] is None:
                continue

            if not any(c["idCompromiso"] == row[22] for c in compromisosJefes):
                compromisosJefes.append({
                    "idCompromiso": row[22],
                    "descripcion": row[23]
                })

        return resultado
    
    @staticmethod
    def createSocializacion(data):
        IdEvaluacion = data["idEvaluacion"]
        existe = EvaluationAdminRepository.existeSocializacion(IdEvaluacion)
        if existe:
            return {
                "existe":"Ya existe una socializacion a esta evaluacion."
            }
        IdSocializador = data["IdSocializador"]   
        IdSocializacion = (EvaluationAdminRepository.crearSocializacion(IdEvaluacion, IdSocializador))
        
        if not data["compromisos"]:
            return
        
        for compromiso in data["compromisos"]:
            EvaluationAdminRepository.compromisoSocializacion(
                IdSocializacion=IdSocializacion,
                compromiso=compromiso
            )