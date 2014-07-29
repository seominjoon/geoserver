from django.core.urlresolvers import reverse
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
            # Actions
            form.save()
            
            # Views
            if request.POST['html'] == 'false':
                return HttpResponse('success')
            else:
                data = {'title': 'Success',
                        'message': 'Question uploaded successfully.',
                        'link': reverse('list'),
                        'linkdes': 'Go to question list page.'}
                return render(request, 'result.html', data)
        else:
            # Do nothing
            
            # Views
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
    # success_url = reverse_lazy('list') # Do I need this?
    slug_field = 'pk'
    
    def delete(self, request, *args, **kwargs):
        # Actions
        self.object = self.get_object()
        self.object.delete()
        
        # Views
        if request.POST['html'] == 'false':
            return HttpResponse('success')
        else:
            data = {'title': 'Success',
                    'message': 'Question deleted successfully.',
                    'link': reverse('list'),
                    'linkdes': 'Go to question list page.',
                    }
            return render(request, 'result.html', data)
    
class QuestionDownloadView(View):
    '''
    QuestionDownloadView is similar to QuestionListView,
    except that download returns JSON while QuestionListView returns HTML.
    Later, this can be combined with  QLV by examining 'html' variable of GET request.
    
    TO BE FIXED:
    Ideally this needs to be implemented with Django REST (serilized JSON data).
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
    
class TagCreateView(CreateView):
    '''
    Create a new tag
    '''
    model = QuestionTag
    fields = ['word']