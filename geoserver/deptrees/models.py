import os
import uuid

from django.db import models


# Create your models here.
class Parser(models.Model):
    '''
    Parser name for DepTree.
    These are pre-defined and usually does not support http update.
    '''
    name = models.CharField(max_length=16)
    
    def __unicode__(self):
        return self.name


def get_image_upload_path(instance, filename):
    type_ = instance.dep_tree.parser
    ext = os.path.splitext(filename)[1]
    return "deptrees/images/%s-%s%s" %(type_, uuid.uuid4(), ext)

class DepTreeImageManager(models.Manager):
    def create_deptree_image(self, image, dep_tree):
        deptree_image = self.create(image=image, dep_tree=dep_tree)
        return deptree_image

class DepTreeImage(models.Model):
    image = models.ImageField(upload_to=get_image_upload_path)
    dep_tree = models.ForeignKey('deptrees.DepTree', related_name='images')
    
    objects = DepTreeImageManager()
    
    def __unicode__(self):
        return "%s-%s" %(self.dep_tree, self.pk)

def get_pickle_upload_path(instance, filename):
    type_ = instance.parser
    ext = os.path.splitext(filename)
    return "deptrees/pickles/%s-%s-%s%s" %(type_, instance.question.pk, uuid.uuid4(), ext)

class DepTree(models.Model):
    '''
    Contains question reference and dep tree images from different parsers
    Either question or text is required; if question is specified,
    the text will be copied as well (TBI)
    '''
    question = models.ForeignKey('questions.Question', null=True, blank=True)
    text = models.TextField()
    parser = models.ForeignKey('deptrees.Parser', related_name='dep_trees')
    graphs_pickle = models.FileField(upload_to=get_pickle_upload_path)
    temp = models.TextField()
    
    # Add pickle here

    '''
    def __unicode__(self):
        return "%s-%s" %(str(self.question.pk),str(self.parser))
    '''
