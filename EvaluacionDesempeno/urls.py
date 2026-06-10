from django.urls import path
from EvaluacionDesempeno.views import FormatoEvaluacion
urlpatterns = [
    path('formato/<int:tipo>/', FormatoEvaluacion),
]

