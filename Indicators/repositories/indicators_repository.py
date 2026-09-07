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