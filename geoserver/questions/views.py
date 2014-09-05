import json

from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, DeleteView, CreateView, UpdateView, \
    View, DetailView

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
        data = {'form': form, 'title':'Upload a question'}
        return  render(request, 'upload_form.html', data)

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
    '''
    def get(self, request, query):
        
        if query == 'all':
            objects = Question.objects.all()
        else:
            try:
                int(query)
            except:
                raise Exception('query must be an integer.')
            objects = [Question.objects.get(pk=int(query))]

        data = [{'pk':question.pk, 'text':question.text, 
                 'diagram_url':question.diagram.url} for question in objects]

        if len(data) == 1:
            data = data[0]

        text = json.dumps(data)
        return HttpResponse(text)

class QuestionUpdateView(UpdateView):
    model = Question
    fields = ['text','diagram']
    template_name_suffix = '_update_form'
    slug_field = 'pk'
   
class QuestionUpdateAllView(View):
    '''
    This view allows user to update multiple questions at the same time
    '''
    def post(self, request):
        pass
    
    def get(self, request):
        forms = []
        for question in Question.objects.all():
            form = QuestionForm(prefix=question.pk, instance=question)
            forms.append(form)
        data = {'title':'Update questions', 'forms':forms}
        return render(request,'update_all_form.html', data)
         
        

    
class QuestionDetailView(DetailView):
    
    model = Question
    context_object_name = 'question'
    slug_field = 'pk'
    
        
class TagCreateView(CreateView):
    '''
    Create a new tag
    '''
    model = QuestionTag
    fields = ['word']