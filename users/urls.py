from django.urls import path
from users.views import LoginView
from users.views import RefreshTokenView, MeView

urlpatterns = [
    path('Login/', LoginView.as_view(), name='login'),
    path('me/', MeView.as_view(), name="myInfo"),
    path("token/refresh/",RefreshTokenView.as_view(),name="token_refresh"),
]
