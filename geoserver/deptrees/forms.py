'''
Created on Jul 22, 2014

@author: minjoon
'''

from django.forms import ModelForm
from deptrees.models import DepTree

class DepTreeForm(ModelForm):
    class Meta:
        model = DepTree
        fields = ['question', 'corenlp_image']
        
