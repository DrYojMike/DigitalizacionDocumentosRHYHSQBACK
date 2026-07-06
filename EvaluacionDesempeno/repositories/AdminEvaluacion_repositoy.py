from django.db import connection

class EvaluationAdminRepository():
    @staticmethod
    def indicadorIndicadoresGestion():
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT IG.[IdEvaIndicadorGestion],
                    IG.[NomEvaIndicadorGestion],
                    COUNT(AUEEMP.NotAutEvaEmpleado) + COUNT(EVAJEF.NotEvaAEmpleado) AS CantEvaluaciones,
                    (COUNT(AUEEMP.NotAutEvaEmpleado) + COUNT(EVAJEF.NotEvaAEmpleado)) * 3 AS NotaMaxima,
                    ISNULL(SUM(AUEEMP.NotAutEvaEmpleado),0) + ISNULL(SUM(EVAJEF.NotEvaAEmpleado),0) AS NotaIndicador,
                    (100*ISNULL(SUM(AUEEMP.NotAutEvaEmpleado),0) + ISNULL(SUM(EVAJEF.NotEvaAEmpleado),0)) / ((COUNT(AUEEMP.NotAutEvaEmpleado) + COUNT(EVAJEF.NotEvaAEmpleado)) * 3) AS Promedio
                FROM [Biometrico].[dbo].[TbEvaluacionIndicadorGestion] IG
                INNER JOIN [Biometrico].[dbo].[TbAutoEvaluacionEmpleado] AUEEMP 
                    ON AUEEMP.IdEvaIndGestion = IG.IdEvaIndicadorGestion
                LEFT JOIN [Biometrico].[dbo].[TbEvaluacionAEmpleado] EVAJEF 
                    ON EVAJEF.IdEvaIndGestion = IG.IdEvaIndicadorGestion
                GROUP BY    
                    IG.IdEvaIndicadorGestion,IG.NomEvaIndicadorGestion
            """)
            return cursor.fetchall()
            
    
    @staticmethod
    def indicadorCompetencia():
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    ECOMP.IdEvaCompetencia,
                    ECOMP.NomEvaCompetencia,
                    COUNT(AUEEMP.NotAutEvaEmpleado) + COUNT(EVAJEF.NotEvaAEmpleado) AS CantEvaluaciones,
                    (COUNT(AUEEMP.NotAutEvaEmpleado) + COUNT(EVAJEF.NotEvaAEmpleado)) * 3 AS NotaMaxima,
                    ISNULL(SUM(AUEEMP.NotAutEvaEmpleado),0) + ISNULL(SUM(EVAJEF.NotEvaAEmpleado),0) AS NotaIndicador,
                    (100*ISNULL(SUM(AUEEMP.NotAutEvaEmpleado),0) + ISNULL(SUM(EVAJEF.NotEvaAEmpleado),0)) / ((COUNT(AUEEMP.NotAutEvaEmpleado) + COUNT(EVAJEF.NotEvaAEmpleado)) * 3) AS Promedio
                FROM [Biometrico].[dbo].[TbEvaluacionIndicadorGestion] IG
                INNER JOIN [Biometrico].[dbo].[TbAutoEvaluacionEmpleado] AUEEMP 
                    ON AUEEMP.IdEvaIndGestion = IG.IdEvaIndicadorGestion
                LEFT JOIN [Biometrico].[dbo].[TbEvaluacionAEmpleado] EVAJEF 
                    ON EVAJEF.IdEvaIndGestion = IG.IdEvaIndicadorGestion
                INNER JOIN [Biometrico].[dbo].[TbEvaluacionCompetencia] ECOMP ON ECOMP.IdEvaCompetencia = IG.IdCompetenciaIndicadorGestion
                GROUP BY    
                    ECOMP.IdEvaCompetencia,
                    ECOMP.NomEvaCompetencia
            """)
            return cursor.fetchall()
    
    
    @staticmethod
    def indicadorArea():
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    EA.IdEvaArea,
                    EA.NomEvaArea,
                    COUNT(AUEEMP.NotAutEvaEmpleado) + COUNT(EVAJEF.NotEvaAEmpleado) AS CantEvaluaciones,
                    (COUNT(AUEEMP.NotAutEvaEmpleado) + COUNT(EVAJEF.NotEvaAEmpleado)) * 3 AS NotaMaxima,
                    ISNULL(SUM(AUEEMP.NotAutEvaEmpleado),0) + ISNULL(SUM(EVAJEF.NotEvaAEmpleado),0) AS NotaIndicador,
                    (100*ISNULL(SUM(AUEEMP.NotAutEvaEmpleado),0) + ISNULL(SUM(EVAJEF.NotEvaAEmpleado),0)) / ((COUNT(AUEEMP.NotAutEvaEmpleado) + COUNT(EVAJEF.NotEvaAEmpleado)) * 3) AS Promedio
                FROM [Biometrico].[dbo].[TbEvaluacionIndicadorGestion] IG
                INNER JOIN [Biometrico].[dbo].[TbAutoEvaluacionEmpleado] AUEEMP 
                    ON AUEEMP.IdEvaIndGestion = IG.IdEvaIndicadorGestion
                LEFT JOIN [Biometrico].[dbo].[TbEvaluacionAEmpleado] EVAJEF 
                    ON EVAJEF.IdEvaIndGestion = IG.IdEvaIndicadorGestion
                INNER JOIN [Biometrico].[dbo].[TbEvaluacionCompetencia] ECOMP ON ECOMP.IdEvaCompetencia = IG.IdCompetenciaIndicadorGestion
                INNER JOIN [Biometrico].[dbo].[TbEvaluacionArea] EA ON EA.IdEvaArea = ECOMP.IdAreaCompetencia  
                GROUP BY    
                    EA.IdEvaArea,
                    EA.NomEvaArea
            """)
            return cursor.fetchall()