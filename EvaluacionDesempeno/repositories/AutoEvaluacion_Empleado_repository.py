from django.db import connection
class AutoEvaluacionEmpleadoReposity:
    
    @staticmethod
    def has_evaluation_this_year(idUsuario):
        with connection.cursor() as cursor:
            cursor.execute("""
                    SELECT TOP 1
                        EG.IdEvaGeneral,
                        EG.FecEvaGeneral,
                        CASE
                            WHEN EG.FecEvaGeneral IS NULL THEN 1
                            WHEN GETDATE() >= DATEADD(YEAR, 1, EG.FecEvaGeneral) THEN 1
                            ELSE 0
                        END AS DebeEvaluarse
                    FROM [Biometrico].[dbo].[Userinfo] U
                    LEFT JOIN [Biometrico].[dbo].[TbAutoEvaluacionEmpleado] AUE
                        ON AUE.IdAutEvaEmpleado = U.UserId
                    LEFT JOIN [Biometrico].[dbo].[TbEvaluacionGeneral] EG
                        ON EG.IdEvaGeneral = AUE.IdEvaGen
                    WHERE U.Userid = %s
                        AND U.FechaRetiro IS NULL
                        AND DATEDIFF(MONTH, U.EmployDate, GETDATE()) >= 6
                        AND U.Mercico = 1
                        AND U.IdCargo <> 31
                    ORDER BY EG.FecEvaGeneral DESC;
            """, [idUsuario])
            row = cursor.fetchone()

            if row is None:
                # No encontró al empleado o no cumple los requisitos
                return False

            return row[2] == 0
    
    
    @staticmethod
    def get_format(tipo):

        with connection.cursor() as cursor:

            cursor.execute("""
                SELECT 
                    A.IdEvaArea,
                    A.NomEvaArea,
                    C.IdEvaCompetencia,
                    C.NomEvaCompetencia,
                    C.DesEvaCompetencia,
                    IG.IdEvaIndicadorGestion,
                    IG.NomEvaIndicadorGestion
                FROM [Biometrico].[dbo].[TbEvaluacionArea] A
                INNER JOIN [Biometrico].[dbo].[TbEvaluacionCompetencia] C ON C.IdAreaCompetencia = A.IdEvaArea
                AND C.ForEvaCompetencia IN (0,%s)
                INNER JOIN [Biometrico].[dbo].[TbEvaluacionIndicadorGestion] IG ON IG.IdCompetenciaIndicadorGestion = C.IdEvaCompetencia AND IG.ForEvaIndicadorGestion IN (0,%s)
                ORDER BY 
                A.IdEvaArea,
                C.IdEvaCompetencia
            """,[tipo,tipo])

            return cursor.fetchall()
     
        
    @staticmethod
    def create_evaluation():
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO [Biometrico].[dbo].[TbEvaluacionGeneral](FecEvaGeneral)
                OUTPUT INSERTED.IdEvaGeneral
                VALUES(GETDATE())
            """)
            row = cursor.fetchone()

            return row[0]
    
    
    @staticmethod
    def create_item_evaluation(nota,id_general,empleado,indicador):
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO [Biometrico].[dbo].[TbAutoEvaluacionEmpleado]
                (NotAutEvaEmpleado,IdEvaGen,IdAutEvaEmpleado,IdEvaIndGestion)
                VALUES(%s,%s,%s,%s)
            """,[nota,id_general,empleado,indicador])
    

    def get_my_evaluations(idUser):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT DISTINCT
                    EVG.IdEvaGeneral,
                    EVG.FecEvaGeneral,
                    U.Name AS empleado,
                    J.Name AS jefe
                FROM [Biometrico].[dbo].[TbEvaluacionGeneral] EVG
                INNER JOIN [Biometrico].[dbo].[TbAutoEvaluacionEmpleado] AEMP ON AEMP.IdEvaGen = EVG.IdEvaGeneral
                INNER JOIN [Biometrico].[dbo].[TbEvaluacionAEmpleado] EJEF ON EJEF.IdEvaGen = EVG.IdEvaGeneral
                INNER JOIN [Biometrico].[dbo].[Userinfo] U ON U.Userid = AEMP.IdAutEvaEmpleado
                INNER JOIN [Biometrico].[dbo].[Userinfo] J ON J.UserId = EJEF.IdEvaEmpJefe
                WHERE U.Userid = %s
            """, [idUser])
            columns = [col[0].lower() for col in cursor.description]
            return[
                dict(zip(columns, row))
                for row in  cursor.fetchall()
            ]
    
    
    @staticmethod
    def evaluacion_info(idEvaluacion):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT
                    U.Name AS EVALUADO
                    ,JEFE.Name AS EVALUADOR
                    ,[FecEvaGeneral]
                    ,EA.IdEvaArea AS IDAREA
                    ,EA.NomEvaArea AS AREA
                    ,EC.IdEvaCompetencia AS IDCOMPETENCIA
                    ,EC.NomEvaCompetencia AS COMPETENCIA
                    ,EC.DesEvaCompetencia AS DESCRIPCION
                    ,IDG.IdEvaIndicadorGestion AS IDINDICADOR
                    ,IDG.NomEvaIndicadorGestion AS INDICADOR
                    ,AE.NotAutEvaEmpleado AS NOTA
                    ,EVAEMP.NotEvaAEmpleado AS NOTAEVALUADA
                    ,COM.IdCompromiso
                    ,COM.DescripcionCompromiso AS COMPROMISO
                FROM [Biometrico].[dbo].[TbEvaluacionGeneral] EG
                INNER JOIN [Biometrico].[dbo].[TbAutoEvaluacionEmpleado] AE ON AE.IdEvaGen = EG.IdEvaGeneral
                INNER JOIN [Biometrico].[dbo].[TbEvaluacionIndicadorGestion] IDG ON IDG.IdEvaIndicadorGestion = AE.IdEvaIndGestion
                INNER JOIN [Biometrico].[dbo].[TbEvaluacionAEmpleado] EVAEMP ON EVAEMP.IdEvaGen = EG.IdEvaGeneral AND IDG.IdEvaIndicadorGestion = EVAEMP.IdEvaIndGestion
                LEFT JOIN [Biometrico].[dbo].[TbEvaluacionCompromisos] COM ON COM.IdEvaGen = EG.IdEvaGeneral
                INNER JOIN [Biometrico].[dbo].[TbEvaluacionCompetencia] EC ON EC.IdEvaCompetencia = IDG.IdCompetenciaIndicadorGestion
                INNER JOIN [Biometrico].[dbo].[TbEvaluacionArea] EA ON EA.IdEvaArea = EC.IdAreaCompetencia
                INNER JOIN [Biometrico].[dbo].[Userinfo] U ON U.Userid = AE.IdAutEvaEmpleado
                INNER JOIN [Biometrico].[dbo].[Userinfo] JEFE ON JEFE.Userid = EVAEMP.IdEvaEmpJefe
                WHERE AE.IdEvaGen = %s            
            """, [idEvaluacion])
            return cursor.fetchall()