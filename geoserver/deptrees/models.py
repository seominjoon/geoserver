from django.db import models
import os
import uuid


# Create your models here.
def get_upload_path(instance, filename, type_):
    ext = os.path.splitext(filename)
    return "deptrees/%s-%s-%s%s" %(type_, instance.question.pk, uuid.uuid4(), ext)

def get_corenlp_upload_path(instance, filename):
    return get_upload_path(instance, filename, 'corenlp')

class DepTree(models.Model):
    '''
    Contains question reference and dep tree images from different parsers
    '''
    question = models.OneToOneField('questions.Question')
    # Dep Tree cosntructed via Stanford CoreNLP
    corenlp_image = models.ImageField(upload_to=get_corenlp_upload_path)
    corenlp_pickle = models.FileField(upload_to=get_corenlp_upload_path)
    
    def __unicode__(self):
        return str(self.question.pk)