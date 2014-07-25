import uuid
import os
import time

from django.core.urlresolvers import reverse
from django.db import models

# Create your models here.

class QuestionTag(models.Model):
    '''
    Tag for grouping questions.
    '''
    word = models.CharField(max_length=32)

def get_upload_path(instance, filename):
    ext = os.path.splitext(filename)[1]
    name = "question-%d-%s%s" %(round(time.time()),uuid.uuid4(), ext)
    return os.path.join('questions', name)

class Question(models.Model):
    '''
    Each question contains text and diagram image.
    Each question is tagged for filtering purpose.
    '''
    text = models.TextField()
    diagram = models.ImageField(upload_to=get_upload_path)
    tag = models.ManyToManyField(QuestionTag)
    
    def __unicode__(self):
        return self.pk
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={'pk', self.pk})
