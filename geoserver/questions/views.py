from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, DeleteView, CreateView, View

from questions.forms import QuestionForm
from questions.models import Question, QuestionTag


# Create your views here.
class QuestionListView(ListView):
    '''
    Display all questions
    '''
    model = Question
    context_object_name = 'question_list'
   
class QuestionUploadView(View):
    def post(self, request):
        form = QuestionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            if request.POST['html'] == 'false':
                return HttpResponse('success')
            else:
                data = {'title': 'Success',
                        'message': 'Question uploaded successfully.',
                        'link': reverse('list'),
                        'linkdes': 'Go to question list page.'}
                return render(request, 'result.html', data)
        else:
            if request.POST['html'] == 'false':
                return HttpResponse('failure')
            else:
                data = {'title': 'Failed',
                        'message': 'Question upload failed.',
                        'link': reverse('upload'),
                        'linkdes': 'Go back and upload the question again.'}
                return render(request, 'result.html', data)

    def get(self, request):
        form = QuestionForm()
        return  render(request, 'upload_form.html', {'form': form, 'title': 'Upload question'})

class QuestionDeleteView(DeleteView):
    model = Question
    success_url = reverse_lazy('list')
    slug_field = 'pk'
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        data = {'title': 'Success',
                'message': 'Question deleted successfully.',
                'link': reverse('list'),
                'linkdes': 'Go to question list page.',
                }
        return render(request, 'result.html', data)
    
class QuestionDownloadView(View):
    '''
    Ideally this needs to be implemented with Django REST (serilized data).
    '''
    def get(self, request, query):
        response = ''
        if query == 'all':
            objects = Question.objects.all()
        else:
            objects = [Question.objects.get(pk=int(query))]
        for question in objects:
            response += "%s,,,%s,,,%s;;;" %(question.pk, question.text, question.diagram.url)
        return HttpResponse(response)
    
class TagAddView(CreateView):
    '''
    Add a new tag
    '''
    model = QuestionTag
    fields = ['word']