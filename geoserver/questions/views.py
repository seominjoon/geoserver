from django.shortcuts import render
from django.views.generic import ListView, DeleteView, View
from django.shortcuts import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy

from questions.models import Question
from questions.forms import QuestionForm

# Create your views here.

class QuestionListView(ListView):
    '''
    Display all questions
    '''
    model = Question
    context_object_name = 'question_list'
   
class QuestionUploadView(View):
    
    #template_name = "questions/upload_form.html"
    
    def post(self, request):
        form = QuestionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('../list')
        else:
            return HttpResponseRedirect('')

    def get(self, request):
        form = QuestionForm()
        return  render(request, 'questions/upload_form.html', {'form': form})
    
class QuestionDeleteView(DeleteView):
    model = Question
    success_url = reverse_lazy('list')
    slug_field = 'pk'

