from django.urls import path
from Indicators.views import StaffSurnoverView, PerformaneEvaluationView,IndicatorGeneralEvalationView, IndicatorSalaryView

urlpatterns = [
    path('rotacion/', StaffSurnoverView.as_view(), name='IndicadorRotacion'),
    path('evaluacion/general', IndicatorGeneralEvalationView.as_view(), name='IndicadorEvaluation'),
    path('evaluacion/desempno', PerformaneEvaluationView.as_view(), name='IndicadorPerformance'),
    path('salario/', IndicatorSalaryView.as_view(), name='IndicadorSalary'),
]
