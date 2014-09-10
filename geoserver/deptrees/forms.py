'''
Created on Jul 22, 2014

@author: minjoon
'''

from django.forms import ModelForm
from geoserver.deptrees.models import DepTree, DepTreeImage

class DepTreeForm(ModelForm):
    class Meta:
        model = DepTree
        fields = ['question','parser','temp']
        
class DepTreeImageForm(ModelForm):
    class Meta:
        model = DepTreeImage
        fields = ['image','dep_tree']