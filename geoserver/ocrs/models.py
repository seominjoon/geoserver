from django.core.urlresolvers import reverse
from django.db import models


# Create your models here.
class OCRTag(models.Model):
    word = models.CharField(max_length=16)
    
    def __unicode__(self):
        return self.word
    
class OCR(models.Model):
    '''
    Each instance represents a single optical character recognizer.
    They contain information, some in JSON format:
    Date the OCR was added.
    Algorithm used (string),
    Parameters used,
    Weights,
    Number of trained instances for the weights,
    LOOCV result 
    Others can be added in future here.
    '''
    last_modified = models.DateTimeField(auto_now=True)
    
    # JSON fields
    algorithm = models.CharField(max_length=64)
    parameters = models.CharField(max_length=1024)
    weights = models.CharField(max_length=2048)
    train_num = models.IntegerField()
    loocv = models.FloatField()
    
    def __unicode__(self):
        return "%d-%s" %(self.pk, self.algorithm)
    
    def get_absolute_url(self):
        return reverse('ocrs-detail', kwargs={'slug': self.pk})
    