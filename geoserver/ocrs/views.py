import json

from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.generic.base import View

from ocrs.forms import OCRForm, TestCharacterForm
from ocrs.models import OCR
from ocrs.tinyocr_interface import get_ocr, ocr_test_image


# Create your views here.
class OCRUploadView(View):
    def post(self, request):
        form = OCRForm(request.POST, request.FILES)
        if form.is_valid():
            ocr_model = form.save()
            return HttpResponse(str(ocr_model.pk))
        else:
            return HttpResponse('failure')

    def get(self, request):
        form = OCRForm()
        data = {'form': form, 'title':'Upload an OCR algorithm'}
        return  render(request, 'upload_form.html', data)

class OCRDownloadView(View):
    '''
    Return the OCR as string
    '''
    def get(self, request, pk):
        ocr = OCR.objects.get(pk=int(pk))
        ocr_url = request.build_absolute_uri(ocr.ocr_pickle.url)
        data = {'ocr_url':ocr_url}
        text = json.dumps(data)
        return HttpResponse(text)
    
class OCRTestView(View):
    def post(self, request):
        form = TestCharacterForm(request.POST, request.FILES)
        if form.is_valid():
            ocr_model = form.save()
            ocr = get_ocr()
            label, score = ocr_test_image(ocr, ocr_model)
            return HttpResponse(label)
        return HttpResponse('failure')
    
    def get(self, request):
        form = TestCharacterForm()
        data = {'form': form, 'title':'Test OCR'}
        return render(request, 'upload_form.html', data)
        