import json
from django.core.files import File
from django.core.urlresolvers import reverse
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.generic import View, ListView, DeleteView, DetailView
from geosolver.utils.prep import save_image, open_image_from_file
from labels.forms import LabelForm
from labels.geosolver_interface import get_labeled_image
from labels.models import Label
from questions.models import Question, QuestionTag
from questions.views import _get_queries, _filter_questions, QuestionListView


class LabelCreateView(View):

    def post(self, request, slug):

        form = LabelForm(request.POST)
        if form.is_valid():
            question = Question.objects.get(pk=slug)
            text = form.cleaned_data['text']
            image = open_image_from_file(question.diagram)
            label_array = json.loads(form.cleaned_data['text'])
            new_image = get_labeled_image(image, label_array)
            # Do some processing on the image
            _, filepath = save_image(new_image)
            ff = File(open(filepath, 'rb'))
            if Label.objects.filter(question=question).exists():
                label = Label.objects.get(question=question)
                label.text = text
                label.image = ff
            else:
                label = Label(question=question, text=text, image=ff)
            label.save()
            # Remove unlabeled tag
            pk_list = [q.pk for q in Question.objects.all()]
            if QuestionTag.objects.filter(word="unlabeled").exists():
                unlabeled = QuestionTag.objects.get(word="unlabeled")
                question.tags.remove(unlabeled)
                question.save()

            new_slug = pk_list[pk_list.index(int(slug)) + 1]

            kwargs = {'slug': new_slug}
            data = {'title': 'Success',
                    'message': 'Label creation succeeded.',
                    'link': reverse('labels-create', kwargs=kwargs),
                    'linkdes': 'Label the next question.'}
            return render(request, 'result.html', data)
        else:
            data = {'title': 'Failed',
                    'message': form.errors(),
                    'link': reverse('labels-create', kwargs={'slug': slug}),
                    'linkdes': 'Go back and upload the tree again.'}
            return render(request, 'result.html', data)

    def get(self, request, slug):
        question = Question.objects.get(pk=slug)
        if Label.objects.filter(question=question).exists():
            annotation = Label.objects.get(question=question).text
        else:
            annotation = ""
        form = LabelForm(initial={'text': annotation})
        pk_list = [q.pk for q in Question.objects.all()]
        new_slug = pk_list[pk_list.index(int(slug)) + 1]
        kwargs = {'slug': new_slug}
        data = {'question': question, 'form': form, 'next': reverse('labels-create', kwargs=kwargs)}
        return render(request, 'labels/labels_create.html', data)

"""
class LabelListView(ListView):
    '''
    Display all characters
    '''
    model = Label
    context_object_name = 'label_list'
    paginate_by = 20

    def get_queryset(self):
        '''
        # One-time thing
        '''
        if self.kwargs['query'] == 'all':
            return Label.objects.filter(question__valid=True)
        else:
            p, t = _get_queries(self.kwargs['query'])
            questions = _filter_questions(p, t)
            labels = Label.objects.filter(question=questions)

            return labels
"""
class LabelListView(QuestionListView):
    template_name = 'labels/label_list.html'


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

        objects = sorted(objects, key=lambda obj: obj.question.pk)

        data = [label.repr() for label in objects]
        return JsonResponse(data, safe=False)


class LabelDeleteView(DeleteView):
    model = Label
    # success_url = reverse_lazy('list') # Do I need this?
    slug_field = 'question__pk'

    def delete(self, request, *args, **kwargs):
        # Actions
        self.object = self.get_object()
        self.object.delete()

        # Views
        if 'html' in request.POST and request.POST['html'] == 'false':
            return HttpResponse('success')
        else:
            kwargs = {'query': 'all'}
            data = {'title': 'Success',
                    'message': 'Label deleted successfully. Note that the question is NOT deleted.',
                    'link': reverse('labels-list', kwargs=kwargs),
                    'linkdes': 'Go to label list page.',
                    }
            return render(request, 'result.html', data)


class LabelDetailView(DetailView):

    model = Label
    context_object_name = 'label'
    slug_field = 'question__pk'
