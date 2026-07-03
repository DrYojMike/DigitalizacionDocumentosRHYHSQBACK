from django.db import connection

class EvaluacionEmpleadoJefeRepository:
    @staticmethod
    def has_employ_whit_evaluations(jefe):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT TOP 1 1
                FROM [Biometrico].[dbo].[Userinfo] U
                INNER JOIN [Biometrico].[dbo].[Userinfo] J ON J.UserCode = U.IdJefe AND U.Mercico = 1
                WHERE U.FechaRetiro IS NULL  and U.IdJefe = %s
            """,[jefe])
        
            return cursor.fetchone() is not None
    
    @staticmethod
    def list_employes_evaluation(jefe):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT
                    ROW_NUMBER() OVER (ORDER BY U.Userid) AS Contador,
                    ISNULL(EG.IdEvaGeneral,0) AS idEvaGeneral,
                    U.Userid,
                    U.UserCode AS CEDULA,
                    U.Name AS NAME,
                    D.DeptName AS DEPARTAMENTO,
                    C.NomCargo AS CARGO,
                    EG.FecEvaGeneral AS EVALUACION,
                    CASE 
                        WHEN EXISTS (
                            SELECT 1
                            FROM [Biometrico].[dbo].[TbEvaluacionAEmpleado] EJ
                            WHERE EJ.IdEmpleadoEvaluado = U.Userid AND EJ.IdEvaGen = EG.IdEvaGeneral
                        )
                        THEN 1
                        ELSE NULL
                    END AS EVALUADO
                FROM [Biometrico].[dbo].[Userinfo] U
                INNER JOIN [Biometrico].[dbo].[TbCargos] C ON C.IdCargo = U.IdCargo
                INNER JOIN [Biometrico].[dbo].[Dept] D ON D.Deptid = U.Deptid
                LEFT JOIN [Biometrico].[dbo].[Userinfo] J ON J.UserCode = U.IdJefe AND U.Mercico = 1
                LEFT JOIN [Biometrico].[dbo].[TbAutoEvaluacionEmpleado] E ON E.IdAutEvaEmpleado = U.UserId
                LEFT JOIN [Biometrico].[dbo].[TbEvaluacionGeneral] EG ON EG.IdEvaGeneral = E.IdEvaGen
                WHERE U.FechaRetiro IS NULL AND U.IdJefe = %s
                GROUP BY
                    U.Userid,
                    U.UserCode,
                    U.Name,
                    D.DeptName,
                    C.NomCargo,
                    EG.FecEvaGeneral,
                    EG.IdEvaGeneral
            """, [jefe])

            columns = [col[0].lower() for col in cursor.description]
            return[
                dict(zip(columns, row))
                for row in  cursor.fetchall()
            ]
            
    @staticmethod
    def get_evaluacio_empleado(idEvaGen):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT [IdEvaGeneral]
                    ,[FecEvaGeneral]
                    ,EA.IdEvaArea AS IDAREA
                    ,EA.NomEvaArea AS AREA
                    ,EC.IdEvaCompetencia AS IDCOMPETENCIA
                    ,EC.NomEvaCompetencia AS COMPETENCIA
                    ,EC.DesEvaCompetencia AS DESCRIPCION
                    ,IDG.IdEvaIndicadorGestion AS IDINDICADOR
                    ,IDG.NomEvaIndicadorGestion AS INDICADOR
                    ,AE.NotAutEvaEmpleado AS NOTA
                    ,U.Userid AS IDUSUARIO
                    ,JEFE.Userid AS IDJEFE
                FROM [Biometrico].[dbo].[TbEvaluacionGeneral] EG
                INNER JOIN [Biometrico].[dbo].[TbAutoEvaluacionEmpleado] AE ON AE.IdEvaGen = EG.IdEvaGeneral
                INNER JOIN [Biometrico].[dbo].[TbEvaluacionIndicadorGestion] IDG ON IDG.IdEvaIndicadorGestion = AE.IdEvaIndGestion
                INNER JOIN [Biometrico].[dbo].[TbEvaluacionCompetencia] EC ON EC.IdEvaCompetencia = IDG.IdCompetenciaIndicadorGestion
                INNER JOIN [Biometrico].[dbo].[TbEvaluacionArea] EA ON EA.IdEvaArea = EC.IdAreaCompetencia
                INNER JOIN [Biometrico].[dbo].[Userinfo] U ON U.Userid = AE.IdAutEvaEmpleado
                INNER JOIN [Biometrico].[dbo].[Userinfo] JEFE ON JEFE.UserCode = U.IdJefe
                WHERE AE.IdEvaGen = %s
            """,[idEvaGen])
            
            return cursor.fetchall()
    
    @staticmethod
    def evaluate_a_employee(nota, idEva, idJefe, idEmp, idIndicador):
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO [Biometrico].[dbo].[TbEvaluacionAEmpleado](NotEvaAEmpleado, IdEvaGen, IdEvaEmpJefe, IdEmpleadoEvaluado, IdEvaIndGestion)
                VALUES(%s, %s, %s, %s, %s)
            """,[nota, idEva, idJefe, idEmp, idIndicador]) 
    
    @staticmethod
    def compromisos_evaluate_a_employe(idEva,idJefe,compromiso):
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO [Biometrico].[dbo].[TbEvaluacionCompromisos](IdEvaGen,IdJefe,DescripcionCompromiso)
                VALUES(%s,%s,%s)
            """, [idEva,idJefe,compromiso])