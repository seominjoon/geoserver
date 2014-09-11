from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.generic.base import View

from ocrs.forms import OCRForm
from ocrs.models import OCR


# Create your views here.
class OCRUploadView(View):
    def post(self, request):
        form = OCRForm(request.POST, request.FILES)
        print request.POST
        if form.is_valid():
            ocr = form.save()
            return HttpResponse(str(ocr.pk))
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

        return HttpResponse(ocr.ocr)