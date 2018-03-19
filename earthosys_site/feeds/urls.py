from django.urls import path
from .views import FeedsView

urlpatterns = [
    path('<int:id>/', FeedsView.as_view(), name='feeds')
]
