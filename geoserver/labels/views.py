import json
import tempfile
import cv2
from django.core.files import File
from django.core.urlresolvers import reverse
from django.db.models.fields.files import FieldFile
from django.shortcuts import render

# Create your views here.
from django.views.generic import View, ListView
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
            print(ff)
            label = Label(question=question, text=form.cleaned_data['text'], image=ff)
            label.save()
            print(label.image)
            data = {'title': 'Success',
                    'message': 'Label creation succeeded.',
                    'link': '',#reverse('deptrees-list'),
                    'linkdes': 'Go to tree list page.'}
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
        data = {'question': question, 'form': form, }
        return render(request, 'labels/labels_create.html', data)

class LabelListView(ListView):
    '''
    Display all characters
    '''
    model = Label
    context_object_name = 'label_list'
