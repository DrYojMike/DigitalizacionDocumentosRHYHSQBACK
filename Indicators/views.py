from django.shortcuts import render
from Indicators.services.indicators_service import IndicatorsService
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

class StaffSurnoverView(APIView):
    def get(self, request):
        try:
            data = IndicatorsService.getStaffTurnover()
            return Response({
                "message":"Indicador de rotacion de personal obtenido con exito.",
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
            

class PerformaneEvaluationView(APIView):
    def get(self, request):
        try:
            data = IndicatorsService.getPerformanceEvaluation()
            return Response({
                "message":"Indicador de Evaluacion de desempeño obtenido con exito.",
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
            

class IndicatorGeneralEvalationView(APIView):
    def get(self, request):
        try:
            data = IndicatorsService.getIndicadorEvaluation()
            return Response({
                "message":"Indicador de Evaluacion de desempeño obtenido con exito.",
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