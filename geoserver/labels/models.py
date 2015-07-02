import json
import os
import uuid
from django.db import models


def get_image_upload_path(instance, filename):
    id_ = uuid.uuid4()
    ext = os.path.splitext(filename)[1]
    return "labels/images/%s%s" % (id_, ext)

# Create your models here.
class Label(models.Model):
    '''
    Label for each question.
    '''
    question = models.OneToOneField('questions.Question', null=True, blank=True, related_name='label')
    text = models.TextField()
    image = models.ImageField(upload_to=get_image_upload_path)


    def __unicode__(self):
        return self.question.__unicode__()


    def dict(self):
        label_data = json.loads(self.text)
        return {'question_pk': self.question.pk,
                'pk': self.pk,
                'label_data': label_data}