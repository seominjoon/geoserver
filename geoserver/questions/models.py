import os
import time
import uuid

from django.core.urlresolvers import reverse
from django.db import models


# Create your models here.
class QuestionTag(models.Model):
    '''
    Tag for grouping questions.
    '''
    word = models.CharField(max_length=16)
    
    def __unicode__(self):
        return self.word


def get_upload_path(instance, filename):
    '''
    Upload path function for Question model
    '''
    ext = os.path.splitext(filename)[1]
    name = "question-%d-%s%s" %(round(time.time()),uuid.uuid4(), ext)
    return os.path.join('questions', name)

class Question(models.Model):
    '''
    Each question contains text and diagram image.
    Each question is tagged for filtering purpose.
    Each question can have more than one tags (thus M2M relationship).
    '''
    text = models.TextField()
    diagram = models.ImageField(upload_to=get_upload_path)
    tags = models.ManyToManyField(QuestionTag)
    
    def __unicode__(self):
        return str(self.pk)
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={'slug': self.pk})
