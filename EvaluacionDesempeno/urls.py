from django.urls import path
from EvaluacionDesempeno.views import FormatoEvaluacionView, CreateEvaluationView, ListaEmpleadoEvaluacionView, EvaluacionEmpleado, EvaluarEmpleadoView,EvaluacionCompletaView,MyListEvaluationsView

urlpatterns = [
    path('formato/<int:tipo>/', FormatoEvaluacionView.as_view(), name="evaluacion"),
    path("evaluations/create/",CreateEvaluationView.as_view(), name="autoevaluacion"),
    path("list/empleados/<str:jefe>/",ListaEmpleadoEvaluacionView.as_view(), name="listaEmpleadosEvaluar"),
    path("autoevaluacion/empleado/<str:idUsuario>/",EvaluacionEmpleado.as_view(), name="autoevaluacionempleado"),
    path("evaluar-empleado/",EvaluarEmpleadoView.as_view(),name="evaluarEmpleado"),
    path("evaluacion/<int:idEvaluacion>/", EvaluacionCompletaView.as_view(), name="evaluacionempleado"),
    path("my/evaluations/<str:idUsuario>/",MyListEvaluationsView.as_view(), name="myevaluations")
]

