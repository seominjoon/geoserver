from django.forms import ModelForm
from labels.models import Label

__author__ = 'minjoon'

class LabelForm(ModelForm):
    class Meta:
        model = Label
        fields = ['text']
