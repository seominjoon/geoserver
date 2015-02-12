import json
from django.core.files import File
from django.core.urlresolvers import reverse
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import View, ListView, UpdateView
from geosolver.utils import save_image, open_image_from_file
from labels.forms import LabelForm
from labels.geosolver_interface import get_labeled_image
from labels.models import Label
from questions.models import Question

class LabelCreateView(View):

    def post(self, request, slug):

        form = LabelForm(request.POST)
        if form.is_valid():
            question = Question.objects.get(pk=slug)
            image = open_image_from_file(question.diagram)
            label_array = json.loads(form.cleaned_data['text'])
            new_image = get_labeled_image(image, label_array)
            # Do some processing on the image
            _, filepath = save_image(new_image)
            ff = File(open(filepath, 'rb'))
            label = Label(question=question, text=form.cleaned_data['text'], image=ff)
            label.save()
            kwargs = {'slug': str(int(slug)+1)}
            data = {'title': 'Success',
                    'message': 'Label creation succeeded.',
                    'link': reverse('labels-create', kwargs=kwargs),
                    'linkdes': 'Label the next question.'}
            return render(request, 'result.html', data)
        else:
            data = {'title': 'Failed',
                    'message': form.errors(),
                    'link': reverse('labels-create'),
                    'linkdes': 'Go back and upload the tree again.'}
            return render(request, 'result.html', data)

    def get(self, request, slug):
        question = Question.objects.get(pk=slug)
        form = LabelForm()
        kwargs = {'slug': str(int(slug)+1)}
        data = {'question': question, 'form': form, 'next': reverse('labels-create', kwargs=kwargs)}
        return render(request, 'labels/labels_create.html', data)


class LabelListView(ListView):
    '''
    Display all characters
    '''
    model = Label
    context_object_name = 'label_list'


class LabelDownloadView(View):
    '''
    LabelDownloadView is similar to QuestionListView,
    except that download returns JSON while QuestionListView returns HTML.
    '''
    def get(self, request, query):

        if query == 'all':
            objects = Label.objects.all()
        else:
            try:
                int(query)
            except:
                raise Exception('query must be an integer.')
            question = Question.objects.get(pk=int(query))
            objects = Label.objects.filter(question=question)

        data = [label.repr() for label in objects]
        return JsonResponse(data, safe=False)
