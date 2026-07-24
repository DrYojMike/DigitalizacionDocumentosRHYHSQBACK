from django.db import connection

class EvaluationAdminRepository():
    @staticmethod
    def indicadorIndicadoresGestion():
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT
                    YEAR(EG.FecEvaGeneral) AS Año,
                    IG.IdEvaIndicadorGestion,
                    IG.NomEvaIndicadorGestion,
                    COUNT(AUEEMP.NotAutEvaEmpleado) + COUNT(EVAJEF.NotEvaAEmpleado) AS CantEvaluaciones,
                    (COUNT(AUEEMP.NotAutEvaEmpleado) + COUNT(EVAJEF.NotEvaAEmpleado)) * 3 AS NotaMaxima,
                    ISNULL(SUM(AUEEMP.NotAutEvaEmpleado),0) + ISNULL(SUM(EVAJEF.NotEvaAEmpleado),0) AS NotaIndicador,
                    (100*ISNULL(SUM(AUEEMP.NotAutEvaEmpleado),0) + ISNULL(SUM(EVAJEF.NotEvaAEmpleado),0)) / ((COUNT(AUEEMP.NotAutEvaEmpleado) + COUNT(EVAJEF.NotEvaAEmpleado)) * 3) AS Promedio
                FROM [Biometrico].[dbo].[TbEvaluacionGeneral] EG 
                LEFT JOIN [Biometrico].[dbo].[TbAutoEvaluacionEmpleado] AUEEMP ON AUEEMP.IdEvaGen = EG.IdEvaGeneral
                LEFT JOIN [Biometrico].[dbo].[TbEvaluacionAEmpleado] EVAJEF ON EVAJEF.IdEvaGen = AUEEMP.IdEvaGen JOIN [Biometrico].[dbo].[TbEvaluacionIndicadorGestion] IG ON IG.IdEvaIndicadorGestion = AUEEMP.IdEvaIndGestion OR IG.IdEvaIndicadorGestion = EVAJEF.IdEvaGen
                LEFT JOIN [Biometrico].[dbo].[TbEvaluacionCompetencia] ECOMP ON ECOMP.IdEvaCompetencia = IG.IdCompetenciaIndicadorGestion
                LEFT JOIN [Biometrico].[dbo].[TbEvaluacionArea] EA  ON EA.IdEvaArea = ECOMP.IdAreaCompetencia
                GROUP BY    
                    EG.FecEvaGeneral,
                    IG.IdEvaIndicadorGestion,
                    IG.NomEvaIndicadorGestion
                ORDER BY IG.IdEvaIndicadorGestion ASC
            """)
            return cursor.fetchall()
            
    
    @staticmethod
    def indicadorCompetencia():
        with connection.cursor() as cursor:
            cursor.execute("""
             SELECT
                    YEAR(EG.FecEvaGeneral) AS Año,
                    ECOMP.IdEvaCompetencia,
                    ECOMP.NomEvaCompetencia,
                    ECOMP.DesEvaCompetencia,
                    COUNT(AUEEMP.NotAutEvaEmpleado) + COUNT(EVAJEF.NotEvaAEmpleado) AS CantEvaluaciones,
                    (COUNT(AUEEMP.NotAutEvaEmpleado) + COUNT(EVAJEF.NotEvaAEmpleado)) * 3 AS NotaMaxima,
                    ISNULL(SUM(AUEEMP.NotAutEvaEmpleado),0) + ISNULL(SUM(EVAJEF.NotEvaAEmpleado),0) AS NotaIndicador,
                    (100*ISNULL(SUM(AUEEMP.NotAutEvaEmpleado),0) + ISNULL(SUM(EVAJEF.NotEvaAEmpleado),0)) / ((COUNT(AUEEMP.NotAutEvaEmpleado) + COUNT(EVAJEF.NotEvaAEmpleado)) * 3) AS Promedio
                FROM [Biometrico].[dbo].[TbEvaluacionGeneral] EG 
                LEFT JOIN [Biometrico].[dbo].[TbAutoEvaluacionEmpleado] AUEEMP ON AUEEMP.IdEvaGen = EG.IdEvaGeneral
                LEFT JOIN [Biometrico].[dbo].[TbEvaluacionAEmpleado] EVAJEF ON EVAJEF.IdEvaGen = AUEEMP.IdEvaGen JOIN [Biometrico].[dbo].[TbEvaluacionIndicadorGestion] IG ON IG.IdEvaIndicadorGestion = AUEEMP.IdEvaIndGestion OR IG.IdEvaIndicadorGestion = EVAJEF.IdEvaGen
                LEFT JOIN [Biometrico].[dbo].[TbEvaluacionCompetencia] ECOMP ON ECOMP.IdEvaCompetencia = IG.IdCompetenciaIndicadorGestion
                LEFT JOIN [Biometrico].[dbo].[TbEvaluacionArea] EA  ON EA.IdEvaArea = ECOMP.IdAreaCompetencia
                GROUP BY    
                    EG.FecEvaGeneral,
                    ECOMP.IdEvaCompetencia,
                    ECOMP.NomEvaCompetencia,
                    ECOMP.DesEvaCompetencia
                ORDER BY ECOMP.IdEvaCompetencia ASC
            """)
            return cursor.fetchall()
    
    
    @staticmethod
    def indicadorArea():
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT
                    YEAR(EG.FecEvaGeneral) AS Año,
                    EA.IdEvaArea,
                    EA.NomEvaArea,
                    COUNT(AUEEMP.NotAutEvaEmpleado) + COUNT(EVAJEF.NotEvaAEmpleado) AS CantEvaluaciones,
                    (COUNT(AUEEMP.NotAutEvaEmpleado) + COUNT(EVAJEF.NotEvaAEmpleado)) * 3 AS NotaMaxima,
                    ISNULL(SUM(AUEEMP.NotAutEvaEmpleado),0) + ISNULL(SUM(EVAJEF.NotEvaAEmpleado),0) AS NotaIndicador,
                    (100*ISNULL(SUM(AUEEMP.NotAutEvaEmpleado),0) + ISNULL(SUM(EVAJEF.NotEvaAEmpleado),0)) / ((COUNT(AUEEMP.NotAutEvaEmpleado) + COUNT(EVAJEF.NotEvaAEmpleado)) * 3) AS Promedio
                FROM [Biometrico].[dbo].[TbEvaluacionGeneral] EG 
                LEFT JOIN [Biometrico].[dbo].[TbAutoEvaluacionEmpleado] AUEEMP ON AUEEMP.IdEvaGen = EG.IdEvaGeneral
                LEFT JOIN [Biometrico].[dbo].[TbEvaluacionAEmpleado] EVAJEF ON EVAJEF.IdEvaGen = AUEEMP.IdEvaGen JOIN [Biometrico].[dbo].[TbEvaluacionIndicadorGestion] IG ON IG.IdEvaIndicadorGestion = AUEEMP.IdEvaIndGestion OR IG.IdEvaIndicadorGestion = EVAJEF.IdEvaGen
                LEFT JOIN [Biometrico].[dbo].[TbEvaluacionCompetencia] ECOMP ON ECOMP.IdEvaCompetencia = IG.IdCompetenciaIndicadorGestion
                LEFT JOIN [Biometrico].[dbo].[TbEvaluacionArea] EA  ON EA.IdEvaArea = ECOMP.IdAreaCompetencia
                GROUP BY    
                    EG.FecEvaGeneral,
                    EA.IdEvaArea,
                    EA.NomEvaArea
                ORDER BY EA.IdEvaArea ASC
            """)
            return cursor.fetchall()
        
    @staticmethod
    def EvaluationEmployeList(userDocumento):
        with connection.cursor() as cursor:
            cursor.execute(
                """
                    SELECT
                        EVG.IdEvaGeneral,
                        EVG.FecEvaGeneral,
                        EMP.IdAutEvaEmpleado,
                        U.Name,
                        U.UserCode,
                        UJEF.Name,
                        UJEF.UserCode,
                        S.IdSoci,
                        SOCI.Name
                    FROM [Biometrico].[dbo].[TbEvaluacionGeneral] EVG
                    LEFT JOIN [Biometrico].[dbo].[TbAutoEvaluacionEmpleado] EMP ON EMP.IdEvaGen = EVG.IdEvaGeneral
                    LEFT JOIN [Biometrico].[dbo].[TbEvaluacionAEmpleado] JEF
                        ON JEF.IdEmpleadoEvaluado = EMP.IdAutEvaEmpleado AND JEF.IdEvaIndGestion = EMP.IdEvaIndGestion
                    LEFT JOIN [Biometrico].[dbo].[TbEvaluacionIndicadorGestion] ING ON ING.IdEvaIndicadorGestion = EMP.IdEvaIndGestion
                    LEFT JOIN [Biometrico].[dbo].[Userinfo] U ON U.UserId = EMP.IdAutEvaEmpleado
                    LEFT JOIN [Biometrico].[dbo].[Userinfo] UJEF ON UJEF.UserId = JEF.IdEvaEmpJefe 
                    LEFT JOIN [Biometrico].[dbo].[TbSocializacionEvDesempeno] S ON S.IdEvaGenSoci = EVG.IdEvaGeneral
                    LEFT JOIN [Biometrico].[dbo].[Userinfo] SOCI ON SOCI.UserId =  S.IdSocializador
                    WHERE U.UserCode = %s
                    GROUP BY
                        EVG.IdEvaGeneral,
                        EVG.FecEvaGeneral,
                        EMP.IdAutEvaEmpleado,
                        U.Name,
                        U.UserCode,
                        UJEF.Name,
                        UJEF.UserCode,
                        S.IdSoci,
                        SOCI.Name
                """,[userDocumento])
            return cursor.fetchall()
    
    
    @staticmethod
    def socializarEmployeEvaluation(idEvaluacion):
        with connection.cursor() as cursor:
            cursor.execute(
                """
                    SELECT
                        EVG.IdEvaGeneral,
                        EVG.FecEvaGeneral,
                        EMP.IdAutEvaEmpleado,
                        U.Name,
                        U.UserCode,
                        UJEF.Name,
                        UJEF.UserCode,
                        AVG(CASE WHEN ING.IdEvaIndicadorGestion IN (13,16,17,19,81,82) THEN (EMP.NotAutEvaEmpleado + JEF.NotEvaAEmpleado) / 2.0 END) / 3.0 * 100 AS Compromiso,
                        AVG(CASE WHEN ING.IdEvaIndicadorGestion IN (15,20,21,22,23,24,27,83) THEN (EMP.NotAutEvaEmpleado + JEF.NotEvaAEmpleado)/2.0 END) / 3.0 * 100 AS Conocimiento,
                        AVG(CASE WHEN ING.IdEvaIndicadorGestion IN (14,25,26) THEN (EMP.NotAutEvaEmpleado + JEF.NotEvaAEmpleado) / 2.0 END) / 3.0 * 100 AS Organizacion,
                        AVG(CASE WHEN ING.IdEvaIndicadorGestion IN (28,29,30,58,84,85,86,108) THEN (EMP.NotAutEvaEmpleado + JEF.NotEvaAEmpleado)/2.0 END) / 3.0 * 100 AS Normas,
                        AVG(CASE WHEN ING.IdEvaIndicadorGestion IN (31,32,33,34,35,36,87,88,89,90,91) THEN (EMP.NotAutEvaEmpleado + JEF.NotEvaAEmpleado) /2.0 END) / 3.0 * 100 AS Liderazgo,
                        AVG(CASE WHEN ING.IdEvaIndicadorGestion IN (37,38,39,40,41,45,46,47,48,49,50,104,105,107,118) THEN (EMP.NotAutEvaEmpleado + JEF.NotEvaAEmpleado) /2.0 END) / 3.0 * 100 AS Comunicacion,
                        AVG(CASE WHEN ING.IdEvaIndicadorGestion IN (69,70,71,72,73,74) THEN (EMP.NotAutEvaEmpleado + JEF.NotEvaAEmpleado) / 2.0 END) / 3.0 * 100 AS Respeto,
                        AVG(CASE WHEN ING.IdEvaIndicadorGestion IN (18,42,43,44,75,76,77,78,79,80) THEN (EMP.NotAutEvaEmpleado + JEF.NotEvaAEmpleado) / 2.0 END) / 3.0 * 100 AS Innovacion,
                        AVG(CASE WHEN ING.IdEvaIndicadorGestion IN (51,52,53,54,55,56,57,115,116,117,119) THEN (EMP.NotAutEvaEmpleado + JEF.NotEvaAEmpleado) / 2.0 END) / 3.0 * 100 AS HSEQ,
                        AVG(CASE WHEN ING.IdEvaIndicadorGestion IN (60,61,62,63,64,109,110,111,112,113,114) THEN (EMP.NotAutEvaEmpleado + JEF.NotEvaAEmpleado) / 2.0 END) / 3.0 * 100 AS GestionHumana,
                        S.IdSoci,
                        SOCI.Name,
                        S.ComproSoci
                    FROM [Biometrico].[dbo].[TbEvaluacionGeneral] EVG
                    INNER JOIN [Biometrico].[dbo].[TbAutoEvaluacionEmpleado] EMP ON EMP.IdEvaGen = EVG.IdEvaGeneral
                    INNER JOIN [Biometrico].[dbo].[TbEvaluacionAEmpleado] JEF
                        ON JEF.IdEmpleadoEvaluado = EMP.IdAutEvaEmpleado AND JEF.IdEvaIndGestion = EMP.IdEvaIndGestion
                    INNER JOIN [Biometrico].[dbo].[TbEvaluacionIndicadorGestion] ING ON ING.IdEvaIndicadorGestion = EMP.IdEvaIndGestion
                    INNER JOIN [Biometrico].[dbo].[Userinfo] U ON U.UserId = EMP.IdAutEvaEmpleado
                    INNER JOIN [Biometrico].[dbo].[Userinfo] UJEF ON UJEF.UserId = JEF.IdEvaEmpJefe
                    LEFT JOIN [Biometrico].[dbo].[TbSocializacionEvDesempeno] S ON S.IdEvaGenSoci = EVG.IdEvaGeneral
                    LEFT JOIN [Biometrico].[dbo].[Userinfo] SOCI ON SOCI.UserId =  S.IdSocializador
                    WHERE EVG.IdEvaGeneral = %s
                    GROUP BY
                        EVG.IdEvaGeneral,
                        EVG.FecEvaGeneral,
                        EMP.IdAutEvaEmpleado,
                        U.Name,
                        U.UserCode,
                        UJEF.Name,
                        UJEF.UserCode,
                        S.IdSoci,
                        SOCI.Name,
                        S.ComproSoci
                """[idEvaluacion]) 
            return cursor.fetchall()