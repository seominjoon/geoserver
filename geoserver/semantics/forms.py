from django.forms import ModelForm
from semantics.models import SemanticParse

__author__ = 'minjoon'


class SemanticParseForm(ModelForm):
    class Meta:
        model = SemanticParse
        fields = ['text_formulas']
