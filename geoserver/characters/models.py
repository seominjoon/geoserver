import os
import time
import uuid

from PIL import Image
from django.core.files.base import File
from django.core.urlresolvers import reverse
from django.db import models

# import tinyocr.utils


# Create your models here.
class CharacterTag(models.Model):
    word = models.CharField(max_length=16)
    
    def __unicode__(self):
        return self.word
    
def get_upload_path(instance, filename):
    '''
    Upload path function for Character model.
    '''
    ext = os.path.splitext(filename)[1]
    name = "character-%d-%s%s" %(round(time.time()),uuid.uuid4(),ext)
    return os.path.join('characters', name)

class Character(models.Model):
    '''
    Each Char contains image, label, and tags.
    Each Char can have more than one tags (thus M2M relationship).
    '''
    
    image = models.ImageField(upload_to=get_upload_path)
    neutral_image = models.ImageField(upload_to=get_upload_path)
    label = models.CharField(max_length=1)
    tags = models.ManyToManyField(CharacterTag)
    labeled = models.BooleanField(default=False)
    valid = models.BooleanField(default=True) 
    
    def __unicode__(self):
        return str(self.pk)
    
    def get_absolute_url(self):
        return reverse('questions-detail', kwargs={'slug': self.pk})
    
    def neutralize_image(self, ext='.png'):
        with self.image:
            with tinyocr.utils.neutralize_image(self.image) as f:
                with File(f) as df:
                    with self.neutral_image:
                        self.neutral_image.save(df.name, df)