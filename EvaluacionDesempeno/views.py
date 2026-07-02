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
                "data":[]
            })
        try:
            data = AutoEvaluacionService.get_evaluation_format(tipo)
            return Response({
                "message":"OK",
                "data":data
            })
        except Exception as e:
            return Response({
                "message":str(e),
                "data":[]
            })


class CreateEvaluationView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsCustomAuthenticated]
    def post(self,request):
        result = AutoEvaluacionService.create_evaluation(request.data)
        if "error" in result:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            result,
            status=status.HTTP_201_CREATED
        )


class ListaEmpleadoEvaluacionView(APIView): 
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsCustomAuthenticated]
    def get(self, request, jefe):
        empleados = EvaluarEmpleadoService.execute(jefe)
        return Response({
            "message":"OK",
            "data":empleados
        })


class EvaluacionEmpleado(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsCustomAuthenticated]
    def get(self, request, idUsuario):
        if not idUsuario:
            return Response({
                "message":
                "Se requiere parametro usuario",

                "data":[]
            })
        
        try:
            data = EvaluarEmpleadoService.get_autoevaluacion_empleado(idUsuario)
            return Response({
                "message":"OK",
                "data":data
            })
        except Exception as e:
            return Response({
                "message":str(e),
                "data":[]
            })
 
 
class EvaluarEmpleadoView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsCustomAuthenticated]
    def post(self, request):
        resultado = EvaluarEmpleadoService.evaluar_empleado(
            request.data
        )
        return Response(
            resultado,
            status=status.HTTP_201_CREATED
        )            
      
        
class EvaluacionCompletaView(APIView): 
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsCustomAuthenticated]
    def get(self, request, idEvaluacion):
        evaluacion = AutoEvaluacionService.get_evaluation_info(idEvaluacion)
        return Response({
            "message":"OK",
            "data":evaluacion
        })


class MyListEvaluationsView(APIView): 
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsCustomAuthenticated]
    def get(self, request, idUsuario):
        evaluaciones = AutoEvaluacionService.list_evaluations(idUsuario)
        return Response({
            "message":"OK",
            "data":evaluaciones
        })