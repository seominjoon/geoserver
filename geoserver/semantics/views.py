import re
from django.core.urlresolvers import reverse
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic import View, ListView
from geoserver.utils import get_next_item
from questions.models import Question
from questions.views import _get_queries, _filter_questions
from semantics.forms import SemanticParseForm
from semantics.models import SemanticParse


class SemanticParseCreateView(View):

    def post(self, request, slug):

        form = SemanticParseForm(request.POST)
        if form.is_valid():
            question = Question.objects.get(pk=slug)
            semantic_parse = SemanticParse(question=question, text_formulas=form.cleaned_data['text_formulas'])
            semantic_parse.save()
            kwargs = {'slug': get_next_item(Question, slug, valid=True)}
            data = {'title': 'Success',
                    'message': 'Semantic parse creation succeeded.',
                    'link': reverse('semantic-parses-create', kwargs=kwargs),
                    'linkdes': 'Create semantic parse for the next question.'}
            return render(request, 'result.html', data)
        else:
            data = {'title': 'Failed',
                    'message': form.errors(),
                    'link': reverse('semantic-parses-create'),
                    'linkdes': 'Go back and upload the tree again.'}
            return render(request, 'result.html', data)

    def get(self, request, slug):
        question = Question.objects.get(pk=slug)
        form = SemanticParseForm()
        kwargs = {'slug': get_next_item(Question, slug, valid=True)}
        data = {'question': question, 'form': form, 'next': reverse('semantic-parses-create', kwargs=kwargs)}
        return render(request, 'semantics/semanticparse_create.html', data)


class SemanticParseListView(ListView):
    '''
    Display all characters
    '''
    model = SemanticParse
    context_object_name = 'semantic_parse_list'

    def get_queryset(self):
        '''
        # One-time thing
        '''
        return SemanticParse.objects.order_by('question__pk')


class SemanticParseDownloadView(View):
    '''
    QuestionDownloadView is similar to QuestionListView,
    except that download returns JSON while QuestionListView returns HTML.
    '''
    def get(self, request, query):

        if query == 'all':
            objects = SemanticParse.objects.all()
        elif re.match(r'^\d+$', query):
            objects = [SemanticParse.objects.get(question__pk=int(query))]
        else:
            p, t = _get_queries(query)
            objects = _filter_questions(p, t)
        data = [parse.text_formulas for parse in objects]
        return JsonResponse(data, safe=False)
