from EvaluacionDesempeno.services.AutoEvaluacion_Empleado_Service import AutoEvaluacionService
from EvaluacionDesempeno.services.Evaluar_Empleado_Jefe_Service import EvaluarEmpleadoService
from users.authentication.custom import CustomJWTAuthentication, IsCustomAuthenticated

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class FormatoEvaluacionView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsCustomAuthenticated]
    def get(self, request, tipo):
        if not tipo:
            return Response({
                "message":"Se requiere parametro tipo",
                "status": status.HTTP_400_BAD_REQUEST,
                "data":[] 
            })
        try:
            data = AutoEvaluacionService.get_evaluation_format(tipo)
            return Response({
                "message":"Formato obtendido con exito",
                "status": status.HTTP_200_OK,
                "data":data
            })
        except Exception as e:
            print(str(e))
            return Response({
                "message":"Ha ocurrido un error interno. Por favor, informe al soporte técnico.",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "data":[]
            })


class CreateEvaluationView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsCustomAuthenticated]
    def post(self,request):
        try:
            result = AutoEvaluacionService.create_evaluation(request.data)
            if "creado" in result:
                return Response({
                    "message":"No puede volver a realizar la evaluacion.",
                    "status":status.HTTP_400_BAD_REQUEST
                })

            return Response(
                result,
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            print(str(e))
            return Response({
                "message":"Ha ocurrido un error interno. Por favor, informe al soporte técnico.",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR
            })


class ListaEmpleadoEvaluacionView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsCustomAuthenticated]
    def get(self, request, jefe):
        try:
            empleados = EvaluarEmpleadoService.execute(jefe)
            return Response({
                "message":"Lista de empleado obtenida de manera correcta.",
                "status": status.HTTP_200_OK,
                "data":empleados
            })
        except Exception as e:
            print(str(e))
            return Response({
                "message":"Ha ocurrido un error interno. Por favor, informe al soporte técnico.",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "data":[]
            })


class EvaluacionEmpleado(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsCustomAuthenticated]
    def get(self, request, idUsuario):
        if not idUsuario:
            return Response({
                "message":"Se requiere parametro usuario",
                "status": status.HTTP_400_BAD_REQUEST,
                "data":[]
            })
        
        try:
            data = EvaluarEmpleadoService.get_autoevaluacion_empleado(idUsuario)
            return Response({
                "message":"La evaluacion del empleado de ha obtenido de manera correcta.",
                "status": status.HTTP_200_OK,
                "data":data
            })
        except Exception as e:
            print(str(e))
            return Response({
                "message":"Ha ocurrido un error interno. Por favor, informe al soporte técnico.",
                "data":[]
            })
 
 
class EvaluarEmpleadoView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsCustomAuthenticated]
    def post(self, request):
        try:
            resultado = EvaluarEmpleadoService.evaluar_empleado(
                request.data
            )
            return Response(
                resultado,
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            print(str(e))
            return Response({
                "message":"Ha ocurrido un error interno. Por favor, informe al soporte técnico.",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "data":[]
            })            
      
        
class EvaluacionCompletaView(APIView): 
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsCustomAuthenticated]
    def get(self, request, idEvaluacion):
        try:
            evaluacion = AutoEvaluacionService.get_evaluation_info(idEvaluacion)
            return Response({
                "message":"Evaluacion obtenida exitosamente.",
                "status": status.HTTP_200_OK,
                "data":evaluacion
            })
        except Exception as e:
            print(str(e))
            return Response({
                "message":"Ha ocurrido un error interno. Por favor, informe al soporte técnico.",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "data":{}
            })


class MyListEvaluationsView(APIView): 
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsCustomAuthenticated]
    def get(self, request, idUsuario):
        try:
            evaluaciones = AutoEvaluacionService.list_evaluations(idUsuario)
            return Response({
                "message":"Listado de evaluaciones Obtenidas de manera correcta",
                "status": status.HTTP_200_OK,
                "data":evaluaciones
            })
        except Exception as e:
            print(str(e))
            return Response({
                "message":"Ha ocurrido un error interno. Por favor, informe al soporte técnico.",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "data":[]
            })