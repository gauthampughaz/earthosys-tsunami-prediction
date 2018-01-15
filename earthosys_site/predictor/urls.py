from django.conf.urls import url
from .views import PredictTsunamiView

app_name = 'predictor'

urlpatterns = [
    url(r'^', PredictTsunamiView.as_view(), name='predict_tsunami')
]