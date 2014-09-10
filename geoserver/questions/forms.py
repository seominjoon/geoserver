'''
Created on Jul 22, 2014

@author: minjoon
'''

from django.forms import ModelForm
from geoserver.questions.models import Question

class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'diagram']
        
