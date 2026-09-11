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

    @staticmethod
    def getIndicadorSalary():
        with connection.cursor() as cursor:
            cursor.execute("""
                DECLARE @BRECHA_SALARIO DECIMAL(18,2) = 500000;
                WITH SalarioMinimoLegal AS (
                    SELECT
                        2025 AS ANO,
                        CAST(1423500 AS DECIMAL(18,2)) AS SALARIO_MINIMO

                    UNION ALL

                    SELECT
                        2026 AS ANO,
                        CAST(1750905 AS DECIMAL(18,2)) AS SALARIO_MINIMO
                ),

                /*
                    Obtiene el salario base mensual de cada empleado.

                    TIPO 01 = SUELDOS
                    TIPO 15 = SALARIO INTEGRAL
                */
                SalariosMensuales AS (
                    SELECT
                        DATEFROMPARTS(YEAR(FECHA), MONTH(FECHA), 1) AS MES,
                        YEAR(FECHA) AS ANO,
                        NOM,
                        SUM(VALOR) AS SALARIO_MENSUAL
                    FROM [EMP002_NOM].[dbo].[NOM_ACUM]
                    WHERE FECHA >= DATEADD(
                            MONTH,
                            -12,
                            DATEFROMPARTS(YEAR(GETDATE()), MONTH(GETDATE()), 1)
                        )
                    AND FECHA < DATEFROMPARTS(
                            YEAR(GETDATE()),
                            MONTH(GETDATE()),
                            1
                        )
                    AND TIPO IN ('01', '15')
                    GROUP BY
                        DATEFROMPARTS(YEAR(FECHA), MONTH(FECHA), 1),
                        YEAR(FECHA),
                        NOM
                ),

                /*
                    Asigna a cada empleado el salario mínimo legal
                    correspondiente al año.
                */
                SalariosConMinimo AS (
                    SELECT
                        S.MES,
                        S.ANO,
                        S.NOM,
                        S.SALARIO_MENSUAL,
                        SM.SALARIO_MINIMO AS SALARIO_MINIMO_LEGAL
                    FROM SalariosMensuales S
                    INNER JOIN SalarioMinimoLegal SM
                        ON SM.ANO = S.ANO
                ),

                /*
                    Resumen mensual.

                    IMPORTANTE:
                    SALARIO_MINIMO ahora es el salario mínimo legal,
                    NO el menor salario encontrado en nómina.
                */
                ResumenMensual AS (
                    SELECT
                        MES,

                        SALARIO_MINIMO_LEGAL,

                        MAX(SALARIO_MENSUAL) AS SALARIO_MAXIMO,

                        AVG(
                            CAST(SALARIO_MENSUAL AS DECIMAL(18,2))
                        ) AS SALARIO_PROMEDIO,

                        COUNT(DISTINCT NOM) AS TOTAL_PERSONAL

                    FROM SalariosConMinimo

                    GROUP BY
                        MES,
                        SALARIO_MINIMO_LEGAL
                ),

                /*
                    Clasificación del personal.
                */
                ClasificacionPersonal AS (
                    SELECT
                        S.MES,
                        S.NOM,
                        S.SALARIO_MENSUAL,

                        CASE
                            /*
                                Si recibió menos del mínimo debido a ingreso,
                                retiro o periodo incompleto, se considera
                                dentro de MINIMO.
                            */
                            WHEN S.SALARIO_MENSUAL <= S.SALARIO_MINIMO_LEGAL
                                THEN 'MINIMO'

                            /*
                                Salario máximo real del mes.
                            */
                            WHEN S.SALARIO_MENSUAL = R.SALARIO_MAXIMO
                                THEN 'MAXIMO'

                            /*
                                Personas dentro de +/- $500.000 del promedio.
                            */
                            WHEN S.SALARIO_MENSUAL BETWEEN
                                    R.SALARIO_PROMEDIO - @BRECHA_SALARIO
                                    AND
                                    R.SALARIO_PROMEDIO + @BRECHA_SALARIO
                                THEN 'PROMEDIO'

                            ELSE 'OTROS'
                        END AS CATEGORIA

                    FROM SalariosConMinimo S

                    INNER JOIN ResumenMensual R
                        ON R.MES = S.MES
                )

                SELECT
                    R.MES,

                    /*
                        Salario mínimo LEGAL vigente para ese año.
                    */
                    R.SALARIO_MINIMO_LEGAL AS SALARIO_MINIMO,

                    /*
                        Cantidad de personas con salario
                        igual o inferior al mínimo legal.
                    */
                    SUM(
                        CASE
                            WHEN C.CATEGORIA = 'MINIMO'
                                THEN 1
                            ELSE 0
                        END
                    ) AS PERSONAL_MINIMO,

                    R.SALARIO_MAXIMO,

                    SUM(
                        CASE
                            WHEN C.CATEGORIA = 'MAXIMO'
                                THEN 1
                            ELSE 0
                        END
                    ) AS PERSONAL_MAXIMO,

                    R.SALARIO_PROMEDIO,

                    SUM(
                        CASE
                            WHEN C.CATEGORIA = 'PROMEDIO'
                                THEN 1
                            ELSE 0
                        END
                    ) AS PERSONAL_PROMEDIO,

                    R.TOTAL_PERSONAL,

                    SUM(
                        CASE
                            WHEN C.CATEGORIA = 'OTROS'
                                THEN 1
                            ELSE 0
                        END
                    ) AS PERSONAL_OTROS

                FROM ResumenMensual R

                LEFT JOIN ClasificacionPersonal C
                    ON C.MES = R.MES

                GROUP BY
                    R.MES,
                    R.SALARIO_MINIMO_LEGAL,
                    R.SALARIO_MAXIMO,
                    R.SALARIO_PROMEDIO,
                    R.TOTAL_PERSONAL

                ORDER BY
                    R.MES ASC;
            """)
            return cursor.fetchall()