from django.urls import path
from .views import HomeView

urlpatterns = [
    path('<int:id>/', HomeView.as_view(), name='feeds')
]
