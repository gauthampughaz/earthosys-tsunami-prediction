from django.urls import path
from .views import FeedsView

urlpatterns = [
    path('', FeedsView.as_view(), name='feeds')
]
