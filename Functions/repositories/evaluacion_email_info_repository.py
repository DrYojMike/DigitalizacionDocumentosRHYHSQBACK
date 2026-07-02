from django.db import connection

class EvaluationEmailInfoRepository:
    @staticmethod
    def get_employee_and_manager(id_empleado):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT
                    EMP.Name,
                    EMP.Email,
                    JEF.Name
                FROM [Biometrico].[dbo].[Userinfo] EMP
                INNER JOIN [Biometrico].[dbo].[Userinfo] JEF ON JEF.UserCode = EMP.IdJefe
                WHERE EMP.UserId = %s
            """, [id_empleado])

            row = cursor.fetchone()

            if not row:
                return None

            return {
                "employee_name": row[0],
                "employee_email": row[1],
                "manager_name": row[2]
            }