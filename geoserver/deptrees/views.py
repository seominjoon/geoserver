from django.core.urlresolvers import reverse
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.generic import View
from django.views.generic.list import ListView

from deptrees.forms import DepTreeForm
from deptrees.models import DepTree


# Create your views here.
class DepTreeUploadView(View):
    '''
    No html-based upload view exists.
    Must be automated via a program.
    '''
    
    def post(self, request):
        form = DepTreeForm(request.POST, request.FILES)
        print request.POST
        print request.FILES
        if form.is_valid():
            form.save()
            if request.POST['html'] == 'false':
                return HttpResponse('success')
            else:
                data = {'title': 'Success',
                        'message': 'Dep tree uploaded successfully.',
                        'link': reverse('list'),
                        'linkdes': 'Go to tree list page.'}
                return render(request, 'result.html', data)
        else:
            if request.POST['html'] == 'false':
                return HttpResponse('failure')
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
   
''' 
    def get_context_data(self, **kwargs):
        context = super(DepTreeListView, self).get_context_data(**kwargs)
        context['text'] = context['question'].text
        return context
'''