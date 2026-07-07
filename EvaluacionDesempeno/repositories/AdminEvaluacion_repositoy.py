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
            print(cursor.fetchall())
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