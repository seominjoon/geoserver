import re
from django.core.urlresolvers import reverse
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import View
from questions.models import Question, Sentence, QuestionTag
from questions.views import _get_queries, _filter_questions
from semantics.forms import SentenceParseForm
from semantics.models import SemanticParse




class SentenceParseAnnotateView(View):
    def get(self, request, question_pk, sentence_index):
        question = Question.objects.get(pk=question_pk)
        sentence = Sentence.objects.get(question=question, index=sentence_index)
        assert not SemanticParse.objects.filter(sentence=sentence).exists()
        form = SentenceParseForm()
        data = {'sentence': sentence, 'form': form, 'next': ''}
        return render(request, 'semantics/sentence_parse_annotate.html', data)

    def post(self, request, question_pk, sentence_index):
        question = Question.objects.get(pk=question_pk)
        sentence = Sentence.objects.get(question=question, index=sentence_index)
        form = SentenceParseForm(request.POST)
        if form.is_valid():
            lines = form.cleaned_data['parses'].split('\r\n')
            valid = True
            invalid_lines = []
            for index, line in enumerate(lines):
                line = line.rstrip().lstrip()
                """
                if not is_valid_annotation(line):
                    valid = False
                    invalid_lines.append(line)
                """

            if valid:
                for index, line in enumerate(lines):
                    line = line.rstrip().lstrip()
                    semantic_parse = SemanticParse(sentence=sentence, number=index, parse=line)
                    semantic_parse.save()

                if len(question.sentences.all()) - 1 == sentence.index:
                    pk_list = [q.pk for q in Question.objects.filter(tags__word="unannotated")]
                    if QuestionTag.objects.filter(word="unannotated").exists() and QuestionTag.objects.filter(word="annotated").exists():
                        unannotated = QuestionTag.objects.get(word="unannotated")
                        annotated = QuestionTag.objects.get(word="annotated")
                        question.tags.remove(unannotated)
                        question.tags.add(annotated)
                        question.save()
                    next_question_pk = pk_list[pk_list.index(int(question_pk)) + 1]
                    next_sentence_index = 0
                else:
                    next_question_pk = question_pk
                    next_sentence_index = "%d" % (int(sentence_index) + 1)

                kwargs = {'question_pk': next_question_pk, 'sentence_index': next_sentence_index}
                data = {'title': 'Success',
                        'message': 'Semantic parses annotated successfully.',
                        'link': reverse('semantics-annotate', kwargs=kwargs),
                        'linkdes': 'Annotate the next sentence.'}
                return render(request, 'result.html', data)

        data = {'title': 'Failed',
                'message': "%r" % (invalid_lines),
                'linkdes': 'Go back and upload the tree again.'}
        return render(request, 'result.html', data)



class SemanticParseDownloadView(View):
    '''
    QuestionDownloadView is similar to QuestionListView,
    except that download returns JSON while QuestionListView returns HTML.
    '''
    def get(self, request, query):

        if query == 'all':
            objects = Question.objects.all()
        elif re.match(r'^\d+$', query):
            objects = [Question.objects.get(pk=int(query))]
        else:
            p, t = _get_queries(query)
            objects = _filter_questions(p, t)
        data = {question.pk: {sentence.index: {parse.number: parse.parse
                                               for parse in sentence.semantic_parses.all()}
                              for sentence in question.sentences.all()}
                for question in objects}
        return JsonResponse(data, safe=False)
