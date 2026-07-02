from Functions.services.email_service import EmailService

class EvaluationEmailService:

    @staticmethod
    def notify_employee(employee_name,employee_email,manager_name):
        asunto = "Nueva evaluación disponible"

        mensaje = f"""
            Hola {employee_name},

            El jefe {manager_name} ha realizado tu evaluación de desempeño.

            Ya puedes ingresar al sistema para revisarla.

            Saludos.
        """
        EmailService.send_email(
            subject=asunto,
            body=mensaje,
            recipients=[employee_email]
        )
        
    @staticmethod
    def notify_AutoEvaluation(employee_name,employee_email):
        asunto = "Haz Realizado Con Exito Tu AutoEvaluacion"
        mensaje = f"""
            Hola {employee_name},

            Tu Autoevaluacion se ha realizado con exito, 
            reseviras un mensaje cuando tu jefe te evalue el desempeño.

            Saludos.
        """
        EmailService.send_email(
            subject=asunto,
            body=mensaje,
            recipients=[employee_email]
        )