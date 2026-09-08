from django.db import connection

class IndicatorsRepository():
    @staticmethod
    def getPerformanceEvaluation():
        with connection.cursor() as cursor:
            cursor.execute("""
                    WITH Base AS
                        (
                            SELECT 
                                A.IdEvaArea,
                                A.NomEvaArea,

                                C.IdEvaCompetencia,
                                C.NomEvaCompetencia,
                                C.DesEvaCompetencia,

                                I.IdEvaIndicadorGestion,
                                I.NomEvaIndicadorGestion,

                                -- 40% empleado + 60% jefe
                                (
                                    ISNULL(AU.NotAutEvaEmpleado, 0) * 0.40
                                    +
                                    ISNULL(EV.NotEvaAEmpleado, 0) * 0.60
                                ) AS NotaPonderada

                            FROM [Biometrico].[dbo].[TbEvaluacionArea] A

                            INNER JOIN [Biometrico].[dbo].[TbEvaluacionCompetencia] C
                                ON C.IdAreaCompetencia = A.IdEvaArea

                            INNER JOIN [Biometrico].[dbo].[TbEvaluacionIndicadorGestion] I
                                ON I.IdCompetenciaIndicadorGestion = C.IdEvaCompetencia

                            LEFT JOIN [Biometrico].[dbo].[TbAutoEvaluacionEmpleado] AU
                                ON AU.IdEvaIndGestion = I.IdEvaIndicadorGestion

                            LEFT JOIN [Biometrico].[dbo].[TbEvaluacionAEmpleado] EV
                                ON EV.IdEvaIndGestion = I.IdEvaIndicadorGestion
                        ),

                        CumplimientoIndicador AS
                        (
                            SELECT
                                *,
                                -- Escala de 1 a 5
                                (NotaPonderada / 3.0) * 100 AS CumplimientoIndicador
                            FROM Base
                        )

                        SELECT
                            IdEvaArea,
                            NomEvaArea,

                            IdEvaCompetencia,
                            NomEvaCompetencia,
                            DesEvaCompetencia,

                            IdEvaIndicadorGestion,
                            NomEvaIndicadorGestion,

                            ROUND(CumplimientoIndicador, 2) AS CumplimientoIndicador,

                            ROUND(
                                AVG(CumplimientoIndicador) 
                                OVER (PARTITION BY IdEvaCompetencia),
                                2
                            ) AS CumplimientoCompetencia,

                            ROUND(
                                AVG(CumplimientoIndicador) 
                                OVER (PARTITION BY IdEvaArea),
                                2
                            ) AS CumplimientoArea

                        FROM CumplimientoIndicador

                        ORDER BY
                            NomEvaArea,
                            NomEvaCompetencia,
                            NomEvaIndicadorGestion;
                """)
            return cursor.fetchall()
        
    @staticmethod
    def getStaffTurnover():
        with connection.cursor() as cursor:
            cursor.execute(
                """
                    DECLARE @FechaActual DATE = CAST(GETDATE() AS DATE);
                    DECLARE @PrimerMes DATE = DATEFROMPARTS(
                        YEAR(@FechaActual),
                        MONTH(@FechaActual),
                        1
                    );
                    ;WITH Meses AS
                    (
                        SELECT 
                            DATEADD(MONTH, -11, @PrimerMes) AS FechaInicio

                        UNION ALL

                        SELECT 
                            DATEADD(MONTH, 1, FechaInicio)
                        FROM Meses
                        WHERE FechaInicio < @PrimerMes
                    ),
                    Datos AS
                    (
                        SELECT
                            M.FechaInicio,
                            EOMONTH(M.FechaInicio) AS FechaFin,
                            (
                                SELECT COUNT(*)
                                FROM Biometrico.dbo.Userinfo U
                                WHERE U.Mercico = 1
                                AND U.EmployDate <= M.FechaInicio
                                AND (
                                        U.FechaRetiro IS NULL
                                        OR U.FechaRetiro >= M.FechaInicio
                                    )
                                AND U.UserCode NOT IN ('1129515772', '1022329491', '11275337')
                            ) AS EmpleadosInicio,
                            (
                                SELECT COUNT(*)
                                FROM Biometrico.dbo.Userinfo U
                                WHERE U.Mercico = 1
                                AND U.EmployDate >= M.FechaInicio
                                AND U.EmployDate <= EOMONTH(M.FechaInicio)
                                AND U.UserCode NOT IN ('1129515772', '1022329491', '11275337')
                            ) AS Ingresos,
                            (
                                SELECT COUNT(*)
                                FROM Biometrico.dbo.Userinfo U
                                WHERE U.Mercico = 1
                                AND U.FechaRetiro >= M.FechaInicio
                                AND U.FechaRetiro <= EOMONTH(M.FechaInicio)
                                AND U.UserCode NOT IN ('1129515772', '1022329491', '11275337')
                            ) AS Retiros,
                            (
                                SELECT COUNT(*)
                                FROM Biometrico.dbo.Userinfo U
                                WHERE U.Mercico = 1
                                AND U.EmployDate <= EOMONTH(M.FechaInicio)
                                AND (
                                        U.FechaRetiro IS NULL
                                        OR U.FechaRetiro > EOMONTH(M.FechaInicio)
                                    )
                                    AND U.UserCode NOT IN ('1129515772', '1022329491', '11275337')
                            ) AS EmpleadosFinal

                        FROM Meses M
                    )
                    SELECT
                        FORMAT(FechaInicio, 'yyyy') AS Periodo,
                        DATENAME(MONTH, FechaInicio) AS Mes,
                        EmpleadosInicio,
                        Ingresos,
                        Retiros,
                        EmpleadosFinal,
                        CAST(
                            (EmpleadosInicio + EmpleadosFinal) / 2.0
                            AS DECIMAL(18,2)
                        ) AS PromedioEmpleados,
                        CAST(
                            CASE
                                WHEN (EmpleadosInicio + EmpleadosFinal) = 0 THEN 0
                                ELSE
                                    (Retiros * 100.0) /
                                    ((EmpleadosInicio + EmpleadosFinal) / 2.0)
                            END
                            AS DECIMAL(10,2)
                        ) AS RotacionPorcentaje
                    FROM Datos
                    ORDER BY FechaInicio
                    OPTION (MAXRECURSION 12);
                """
            )
            
            return cursor.fetchall()
    
    @staticmethod
    def getIndicatorEvaluationGeneral():
        with connection.cursor() as cursor:
            cursor.execute("""           
                SELECT
                    AVG(CASE WHEN ING.IdEvaIndicadorGestion IN (13,16,19,82) THEN (EMP.NotAutEvaEmpleado * 0.40) + (JEF.NotEvaAEmpleado * 0.60) END) / 3.0 * 100 AS 'Eficiencia En El Trabajo',
                    AVG(CASE WHEN ING.IdEvaIndicadorGestion IN (20,21,22,23,24,27,83) THEN (EMP.NotAutEvaEmpleado * 0.40) + (JEF.NotEvaAEmpleado * 0.60) END) / 3.0 * 100 AS 'Conocimientos Tecnicos',
                    AVG(CASE WHEN ING.IdEvaIndicadorGestion IN (14,25,26,39,59,61,62,63) THEN (EMP.NotAutEvaEmpleado * 0.40) + (JEF.NotEvaAEmpleado * 0.60) END ) / 3.0 * 100 AS 'Destreza En La Realizacion Del Trabajo',
                    AVG(CASE WHEN ING.IdEvaIndicadorGestion IN (28,29,30,40,51,52,58,84,85,86,108,115,116) THEN (EMP.NotAutEvaEmpleado * 0.40) + (JEF.NotEvaAEmpleado * 0.60) END) / 3.0 * 100 AS 'Cumplimiento De Normas Y Procedimientos',
                    AVG(CASE WHEN ING.IdEvaIndicadorGestion IN (43,44,87,88,89,90,91) THEN (EMP.NotAutEvaEmpleado * 0.40) + (JEF.NotEvaAEmpleado * 0.60) END) / 3.0 * 100 AS 'Compromiso Organizacional',
                    AVG(CASE WHEN ING.IdEvaIndicadorGestion IN (31,32,33,34,35,37,38,46,47,104,105,107,118) THEN (EMP.NotAutEvaEmpleado * 0.40) + (JEF.NotEvaAEmpleado * 0.60)END) / 3.0 * 100 AS 'Supervision',
                    AVG(CASE WHEN ING.IdEvaIndicadorGestion IN (17,42,76) THEN (EMP.NotAutEvaEmpleado * 0.40) + (JEF.NotEvaAEmpleado * 0.60) END) / 3.0 * 100 AS 'Toma De Decisiones',
                    AVG(CASE WHEN ING.IdEvaIndicadorGestion IN (45,50,81) THEN (EMP.NotAutEvaEmpleado * 0.40) + (JEF.NotEvaAEmpleado * 0.60) END) / 3.0 * 100 AS 'Trabajo En Equipo',
                    AVG(CASE WHEN ING.IdEvaIndicadorGestion IN (53,54,55,60,110,117) THEN (EMP.NotAutEvaEmpleado * 0.40) + (JEF.NotEvaAEmpleado * 0.60) END) / 3.0 * 100 AS 'Direccionamiento Estrategico',
                    AVG(CASE WHEN ING.IdEvaIndicadorGestion IN (56,57,79) THEN (EMP.NotAutEvaEmpleado * 0.40) + (JEF.NotEvaAEmpleado * 0.60) END) / 3.0 * 100 AS 'Participacion Y Capacitacion',
                    AVG(CASE WHEN ING.IdEvaIndicadorGestion IN (18,48,57,75,80,109,111,112,113,114,119) THEN (EMP.NotAutEvaEmpleado * 0.40) + (JEF.NotEvaAEmpleado * 0.60) END) / 3.0 * 100 AS 'Desarrollo De Las Actividades',
                    AVG(CASE WHEN ING.IdEvaIndicadorGestion IN (41,48,49,69,70,71,72,73,74) THEN (EMP.NotAutEvaEmpleado * 0.40) + (JEF.NotEvaAEmpleado * 0.60) END) / 3.0 * 100 AS 'Relaciones Interpersonales',
                    AVG(CASE WHEN ING.IdEvaIndicadorGestion IN (18,42,43,75,77,78) THEN (EMP.NotAutEvaEmpleado * 0.40) + (JEF.NotEvaAEmpleado * 0.60) END) / 3.0 * 100 AS 'Creatividad E Iniciativa'
                FROM [Biometrico].[dbo].[TbEvaluacionGeneral] EVG
                INNER JOIN [Biometrico].[dbo].[TbAutoEvaluacionEmpleado] EMP ON EMP.IdEvaGen = EVG.IdEvaGeneral
                INNER JOIN [Biometrico].[dbo].[TbEvaluacionAEmpleado] JEF ON JEF.IdEmpleadoEvaluado = EMP.IdAutEvaEmpleado AND JEF.IdEvaIndGestion = EMP.IdEvaIndGestion
                INNER JOIN [Biometrico].[dbo].[TbEvaluacionIndicadorGestion] ING ON ING.IdEvaIndicadorGestion = EMP.IdEvaIndGestion;
            """)
            return cursor.fetchall()
            
    @staticmethod
    def getIndicatorEvaluationType2():
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT
                    AVG(CASE WHEN ING.IdEvaIndicadorGestion IN (13,16,19,82) AND ING.ForEvaIndicadorGestion IN (0,2) THEN (EMP.NotAutEvaEmpleado * 0.40) + (JEF.NotEvaAEmpleado * 0.60) END) / 3.0 * 100 AS 'Eficiencia En El Trabajo',
                    AVG(CASE WHEN ING.IdEvaIndicadorGestion IN (20,21,22,23,24,27,83) AND ING.ForEvaIndicadorGestion IN (0,2) THEN (EMP.NotAutEvaEmpleado * 0.40) + (JEF.NotEvaAEmpleado * 0.60) END) / 3.0 * 100 AS 'Conocimientos Tecnicos',
                    AVG(CASE WHEN ING.IdEvaIndicadorGestion IN (14,25,26,39,59,61,62,63) AND ING.ForEvaIndicadorGestion IN (0,2) THEN (EMP.NotAutEvaEmpleado * 0.40) + (JEF.NotEvaAEmpleado * 0.60) END ) / 3.0 * 100 AS 'Destreza En La Realizacion Del Trabajo',
                    AVG(CASE WHEN ING.IdEvaIndicadorGestion IN (28,29,30,40,51,52,58,84,85,86,108,115,116) AND ING.ForEvaIndicadorGestion IN (0,2) THEN (EMP.NotAutEvaEmpleado * 0.40) + (JEF.NotEvaAEmpleado * 0.60) END) / 3.0 * 100 AS 'Cumplimiento De Normas Y Procedimientos',
                    AVG(CASE WHEN ING.IdEvaIndicadorGestion IN (43,44,87,88,89,90,91) AND ING.ForEvaIndicadorGestion IN (0,2) THEN (EMP.NotAutEvaEmpleado * 0.40) + (JEF.NotEvaAEmpleado * 0.60) END) / 3.0 * 100 AS 'Compromiso Organizacional',
                    AVG(CASE WHEN ING.IdEvaIndicadorGestion IN (53,54,55,60,110,117) AND ING.ForEvaIndicadorGestion IN (0,2) THEN (EMP.NotAutEvaEmpleado * 0.40) + (JEF.NotEvaAEmpleado * 0.60) END) / 3.0 * 100 AS 'Direccionamiento Estrategico',
                    AVG(CASE WHEN ING.IdEvaIndicadorGestion IN (56,57,79) AND ING.ForEvaIndicadorGestion IN (0,2) THEN (EMP.NotAutEvaEmpleado * 0.40) + (JEF.NotEvaAEmpleado * 0.60) END) / 3.0 * 100 AS 'Participacion Y Capacitacion',
                    AVG(CASE WHEN ING.IdEvaIndicadorGestion IN (18,48,57,75,80,109,111,112,113,114,119) AND ING.ForEvaIndicadorGestion IN (0,2) THEN (EMP.NotAutEvaEmpleado * 0.40) + (JEF.NotEvaAEmpleado * 0.60) END) / 3.0 * 100 AS 'Desarrollo De Las Actividades',
                    AVG(CASE WHEN ING.IdEvaIndicadorGestion IN (41,48,49,69,70,71,72,73,74) AND ING.ForEvaIndicadorGestion IN (0,2) THEN (EMP.NotAutEvaEmpleado * 0.40) + (JEF.NotEvaAEmpleado * 0.60) END) / 3.0 * 100 AS 'Relaciones Interpersonales',
                    AVG(CASE WHEN ING.IdEvaIndicadorGestion IN (18,42,43,75,77,78) AND ING.ForEvaIndicadorGestion IN (0,2) THEN (EMP.NotAutEvaEmpleado * 0.40) + (JEF.NotEvaAEmpleado * 0.60) END) / 3.0 * 100 AS 'Creatividad E Iniciativa'
                FROM [Biometrico].[dbo].[TbEvaluacionGeneral] EVG
                INNER JOIN [Biometrico].[dbo].[TbAutoEvaluacionEmpleado] EMP ON EMP.IdEvaGen = EVG.IdEvaGeneral
                INNER JOIN [Biometrico].[dbo].[TbEvaluacionAEmpleado] JEF ON JEF.IdEmpleadoEvaluado = EMP.IdAutEvaEmpleado AND JEF.IdEvaIndGestion = EMP.IdEvaIndGestion
                INNER JOIN [Biometrico].[dbo].[TbEvaluacionIndicadorGestion] ING ON ING.IdEvaIndicadorGestion = EMP.IdEvaIndGestion;               
            """)
            return cursor.fetchall()
            
            
    @staticmethod
    def getIndicatorEvaluationType1():
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT
                    AVG(CASE WHEN ING.IdEvaIndicadorGestion IN (13,16,19,82) AND ING.ForEvaIndicadorGestion IN (0,1) THEN (EMP.NotAutEvaEmpleado * 0.40) + (JEF.NotEvaAEmpleado * 0.60) END) / 3.0 * 100 AS 'Eficiencia En El Trabajo',
                    AVG(CASE WHEN ING.IdEvaIndicadorGestion IN (20,21,22,23,24,27,83) AND ING.ForEvaIndicadorGestion IN (0,1) THEN (EMP.NotAutEvaEmpleado * 0.40) + (JEF.NotEvaAEmpleado * 0.60) END) / 3.0 * 100 AS 'Conocimientos Tecnicos',
                    AVG(CASE WHEN ING.IdEvaIndicadorGestion IN (14,25,26,39,59,61,62,63) AND ING.ForEvaIndicadorGestion IN (0,1) THEN (EMP.NotAutEvaEmpleado * 0.40) + (JEF.NotEvaAEmpleado * 0.60) END ) / 3.0 * 100 AS 'Destreza En La Realizacion Del Trabajo',
                    AVG(CASE WHEN ING.IdEvaIndicadorGestion IN (28,29,30,40,51,52,58,84,85,86,108,115,116) AND ING.ForEvaIndicadorGestion IN (0,1) THEN (EMP.NotAutEvaEmpleado * 0.40) + (JEF.NotEvaAEmpleado * 0.60) END) / 3.0 * 100 AS 'Cumplimiento De Normas Y Procedimientos',
                    AVG(CASE WHEN ING.IdEvaIndicadorGestion IN (43,44,87,88,89,90,91) AND ING.ForEvaIndicadorGestion IN (0,1) THEN (EMP.NotAutEvaEmpleado * 0.40) + (JEF.NotEvaAEmpleado * 0.60) END) / 3.0 * 100 AS 'Compromiso Organizacional',
                    AVG(CASE WHEN ING.IdEvaIndicadorGestion IN (31,32,33,34,35,37,38,46,47,104,105,107,118) AND ING.ForEvaIndicadorGestion IN (0,1) THEN (EMP.NotAutEvaEmpleado * 0.40) + (JEF.NotEvaAEmpleado * 0.60)END) / 3.0 * 100 AS 'Supervision',
                    AVG(CASE WHEN ING.IdEvaIndicadorGestion IN (17,42,76) AND ING.ForEvaIndicadorGestion IN (0,1) THEN (EMP.NotAutEvaEmpleado * 0.40) + (JEF.NotEvaAEmpleado * 0.60) END) / 3.0 * 100 AS 'Toma De Decisiones',
                    AVG(CASE WHEN ING.IdEvaIndicadorGestion IN (45,50,81) AND ING.ForEvaIndicadorGestion IN (0,1) THEN (EMP.NotAutEvaEmpleado * 0.40) + (JEF.NotEvaAEmpleado * 0.60) END) / 3.0 * 100 AS 'Trabajo En Equipo',
                    AVG(CASE WHEN ING.IdEvaIndicadorGestion IN (53,54,55,60,110,117) AND ING.ForEvaIndicadorGestion IN (0,1) THEN (EMP.NotAutEvaEmpleado * 0.40) + (JEF.NotEvaAEmpleado * 0.60) END) / 3.0 * 100 AS 'Direccionamiento Estrategico',
                    AVG(CASE WHEN ING.IdEvaIndicadorGestion IN (56,57,79) AND ING.ForEvaIndicadorGestion IN (0,1) THEN (EMP.NotAutEvaEmpleado * 0.40) + (JEF.NotEvaAEmpleado * 0.60) END) / 3.0 * 100 AS 'Participacion Y Capacitacion',
                    AVG(CASE WHEN ING.IdEvaIndicadorGestion IN (18,48,57,75,80,109,111,112,113,114,119) AND ING.ForEvaIndicadorGestion IN (0,1) THEN (EMP.NotAutEvaEmpleado * 0.40) + (JEF.NotEvaAEmpleado * 0.60) END) / 3.0 * 100 AS 'Desarrollo De Las Actividades'
                FROM [Biometrico].[dbo].[TbEvaluacionGeneral] EVG
                INNER JOIN [Biometrico].[dbo].[TbAutoEvaluacionEmpleado] EMP ON EMP.IdEvaGen = EVG.IdEvaGeneral
                INNER JOIN [Biometrico].[dbo].[TbEvaluacionAEmpleado] JEF ON JEF.IdEmpleadoEvaluado = EMP.IdAutEvaEmpleado AND JEF.IdEvaIndGestion = EMP.IdEvaIndGestion
                INNER JOIN [Biometrico].[dbo].[TbEvaluacionIndicadorGestion] ING ON ING.IdEvaIndicadorGestion = EMP.IdEvaIndGestion;
            """)
            return cursor.fetchall()