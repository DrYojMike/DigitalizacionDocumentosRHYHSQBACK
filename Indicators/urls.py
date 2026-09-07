from django.urls import path
from Indicators.views import StaffSurnoverView, PerformaneEvaluationView

urlpatterns = [
    path('rotacion/', StaffSurnoverView.as_view(), name='IndicadorRotacion'),
    path('evaluacion/desempno', PerformaneEvaluationView.as_view(), name='IndicadorPerformance'),
]
