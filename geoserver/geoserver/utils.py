'''
Created on Sep 14, 2014

@author: minjoon
'''
import tempfile

from PIL import Image
from django.core.files.base import File


def neutralize_image(fh, ext='.png'):
    num, filepath= tempfile.mkstemp(suffix=ext)
    image = Image.open(fh)
    image.save(filepath)
    fh.close()
    return File(open(filepath))


def get_next_item(model, pk, **kwargs):
    """
    Get the next item (from pk) in the database that satisfies kwargs.

    :param model:
    :param pk:
    :param kwargs:
    :return:
    """
    objects = model.objects.filter(pk__gt=pk, **kwargs)
    return objects[0]