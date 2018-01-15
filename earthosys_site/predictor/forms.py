from django.forms import ModelForm
from .models import PredictorRecord


class PredictorForm(ModelForm):

    class Meta:
        model = PredictorRecord
        fields = ('magnitude', 'depth', 'latitude', 'longitude')
