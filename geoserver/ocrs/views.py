import json

from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.generic.base import View

from ocrs.forms import OCRForm, TestCharacterForm, OCRForm2, OCRCreateForm
from ocrs.models import OCR, variables
'''
from ocrs.tinyocr_interface import ocr_test_model, unpickle_ocr_manager, \
    create_ocr_manager
'''

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
        ocr = OCR.objects.get(pk=pk)
        ocr_url = request.build_absolute_uri(ocr.ocr_pickle.url)
        data = {'ocr_url':ocr_url}
        text = json.dumps(data)
        return HttpResponse(text)
    
class OCRTestView(View):
    def post(self, request):
        form = TestCharacterForm(request.POST, request.FILES)
        if form.is_valid():
            character_model = form.save()
            ocr_pk = variables['default_ocr_pk']
            ocr = OCR.objects.get(pk=ocr_pk).ocr_manager
            label, scores = ocr_test_model(ocr, character_model)
            return HttpResponse("%s,%f" %(label,scores[label]))
        return HttpResponse('failure')
    
    def get(self, request):
        form = TestCharacterForm()
        data = {'form': form, 'title':'Test OCR', 'button': 'Upload',
                'message': 'Default OCR: %s' %variables['default_ocr_pk']}
        return render(request, 'submit_form.html', data)
    
class OCRUploadView2(View):
    def post(self, request):
        form = OCRForm2(request.POST, request.FILES)
        if form.is_valid():
            ocr_manager = unpickle_ocr_manager(request.FILES['ocr_manager_p'])
            if ocr_manager is not None:
                ocr = OCR()
                ocr.ocr_manager = ocr_manager
                ocr.save() 
                return HttpResponse(ocr.pk)
        return HttpResponse('failure')
    
    def get(self, request):
        form = OCRForm2()
        data = {'form': form, 'title':'Upload an OCR algorithm'}
        return  render(request, 'upload_form.html', data)
    
class OCRCreateView(View):
    '''
    Create a OCR via web GUI, possibly setting parameters in future.
    '''
    def post(self, request):
        form = OCRCreateForm(request.POST, request.FILES)
        if form.is_valid():
            ocr_manager = create_ocr_manager()
            ocr = OCR()
            ocr.ocr_manager = ocr_manager
            ocr.save()
            if request.POST['set_default']:
                variables['default_ocr_pk'] = ocr.pk 
            result = ocr_manager.loocv(include_test=True)
            return HttpResponse(str(result))
        return HttpResponse('failure')
    
    def get(self, request):
        form = OCRCreateForm()
        data = {'form': form, 'title': 'Create an OCR', 'button': 'Create',
                'message': "Default OCR: %s" %variables['default_ocr_pk']}
        return render(request, 'submit_form.html', data)
        