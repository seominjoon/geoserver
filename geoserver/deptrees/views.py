from django.core.urlresolvers import reverse
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.generic import View
from django.views.generic.list import ListView

from deptrees.forms import DepTreeForm, DepTreeImageForm
from deptrees.models import DepTree


# Create your views here.
class DepTreeImageUploadView(View):
    def post(self, request):
        form = DepTreeImageForm(request.POST, request.FILES)
        print request.POST
        if form.is_valid():
            this = form.save()
            if request.POST['html'] == 'false':
                return HttpResponse(str(this.pk))
            else:
                data = {'title': 'Success',
                        'message': 'Dep tree image uploaded successfully.',
                        'link': reverse('list'),
                        'linkdes': 'Go to tree list page.'}
                return render(request, 'result.html', data)
        else:
            if request.POST['html'] == 'false':
                return HttpResponse('-1')
            else:
                data = {'title': 'Failed',
                        'message': 'Dep tree image upload failed.',
                        'link': reverse('image_upload'),
                        'linkdes': 'Go back and upload the tree again.'}
                return render(request, 'result.html', data)

    def get(self, request):
        form = DepTreeImageForm()
        return  render(request, 'upload_form.html', {'form': form, 'title': 'Upload dep tree'})
    

class DepTreeUploadView(View):
    
    def post(self, request):
        form = DepTreeForm(request.POST)
        print request.POST
        if form.is_valid():
            this = form.save()
            if request.POST['html'] == 'false':
                return HttpResponse(str(this.pk))
            else:
                data = {'title': 'Success',
                        'message': 'Dep tree uploaded successfully.',
                        'link': reverse('list'),
                        'linkdes': 'Go to tree list page.'}
                return render(request, 'result.html', data)
        else:
            if request.POST['html'] == 'false':
                return HttpResponse('-1')
            else:
                data = {'title': 'Failed',
                        'message': 'Dep tree upload failed.',
                        'link': reverse('upload'),
                        'linkdes': 'Go back and upload the tree again.'}
                return render(request, 'result.html', data)

    def get(self, request):
        form = DepTreeForm()
        return  render(request, 'upload_form.html', {'form': form, 'title': 'Upload dep tree'})
    
    
class DepTreeListView(ListView):
    model = DepTree
    context_object_name = 'deptree_list'
   
    def get_context_data(self, **kwargs):
        context = super(DepTreeListView, self).get_context_data(**kwargs)
        context['show_img'] = 'false'
        return context