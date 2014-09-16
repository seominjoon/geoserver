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
