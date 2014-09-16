'''
Created on Sep 13, 2014

@author: minjoon
'''
from cPickle import UnpicklingError
import numpy

import cv2
from tinyocr.ocr_manager import OCRManager
from tinyocr.utils import cv2_file_to_array

import cPickle as pickle
from characters.models import Character


def ocr_test_model(ocr, character_model):
    if character_model.neutral_image is None or not bool(character_model.neutral_image):
        character_model.neutralize_image()
    return ocr_test_file(ocr, character_model.neutral_image) 

def ocr_test_file(ocr, image_file):
    return ocr_test_array(ocr, cv2_file_to_array(image_file))
    
def ocr_test_array(ocr, array):
    return ocr.predict(array)

def create_ocr_manager():
    ocrm = OCRManager()
    
    for character in Character.objects.all():
        with character.image:
            if character.valid and character.labeled:
                ocrm.add_image_file(character.image, character.label)
    ocrm.compute_descriptions()
    ocrm.learn() 
    return ocrm

def unpickle_ocr_manager(f):
    '''
    Unpickle a file and check if it is an instance of OCRManager.
    If not, return None
    '''
    try:
        ocr_manager = pickle.load(f)
    except UnpicklingError:
        return None

    if isinstance(ocr_manager, OCRManager):
        return ocr_manager
    return None

    