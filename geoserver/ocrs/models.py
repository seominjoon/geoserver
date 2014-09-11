import os
import time
import uuid

from django.core.urlresolvers import reverse
from django.db import models


# Create your models here.
class OCRTag(models.Model):
    word = models.CharField(max_length=16)
    
    def __unicode__(self):
        return self.word

def get_upload_path(instance, filename):
    '''
    Upload path function for Question model
    '''
    ext = os.path.splitext(filename)[1]
    name = "ocr-%d-%s%s" %(round(time.time()),uuid.uuid4(), ext)
    return os.path.join('ocrs', name)
    
class OCR(models.Model):
    '''
    Each instance represents a single optical character recognizer.
    '''
    last_modified = models.DateTimeField(auto_now=True)
    
    # name 
    ocr_pickle = models.FileField(upload_to=get_upload_path)
    descriptor_name = models.CharField(max_length=64)
    learner_name = models.CharField(max_length=64)
     
    def __unicode__(self):
        return "%d-%s+%s" %(self.pk, self.descriptor_name, self.learner_name)
    
    def get_absolute_url(self):
        return reverse('ocrs-detail', kwargs={'slug': self.pk})
    