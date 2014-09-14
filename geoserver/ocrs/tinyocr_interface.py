'''
Created on Sep 13, 2014

@author: minjoon
'''
import numpy

import cv2
from tinyocr.ocr_manager import OCRManager

import cPickle as pickle
from ocrs.models import OCR


def get_ocr(pk=1):
    ocr_model = OCR.objects.get(pk=pk)
    ocr_f = ocr_model.ocr_pickle
    return pickle.load(ocr_f)

def ocr_test_image(ocr, ocr_model):
    if ocr_model.neutral_image is None or not bool(ocr_model.neutral_image):
        ocr_model.neutralize_image()
    file_bytes = numpy.asarray(bytearray(ocr_model.neutral_image.read()), dtype=numpy.uint8)
    img_data_ndarray = cv2.imdecode(file_bytes, cv2.CV_LOAD_IMAGE_GRAYSCALE)
    return ocr.predict(img_data_ndarray)