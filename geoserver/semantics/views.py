import re
from django.core.urlresolvers import reverse
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import View, ListView
from questions.models import Question, Sentence, QuestionTag, Choice
from questions.views import _get_queries, _filter_questions, QuestionListView
from semantics.forms import SentenceParseForm
from semantics.models import SentenceAnnotation, ChoiceAnnotation


class SentenceParseAnnotateView(View):
    def get(self, request, question_pk, sentence_index):
        question = Question.objects.get(pk=question_pk)
        sentence = Sentence.objects.get(question=question, index=sentence_index)
        if SentenceAnnotation.objects.filter(sentence=sentence).exists():
            annotations = "\n".join(sp.parse for sp in SentenceAnnotation.objects.filter(sentence=sentence))
        else:
            annotations = ""
        form = SentenceParseForm(initial={'parses': annotations})
        data = {'sentence': sentence, 'form': form, 'next': request.META['HTTP_REFERER']}
        return render(request, 'semantics/sentenceparse_annotate.html', data)

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
                    if SentenceAnnotation.objects.filter(sentence=sentence, number=index).exists():
                        sentence_annotation = SentenceAnnotation.objects.get(sentence=sentence, number=index)
                        sentence_annotation.annotation = line
                    else:
                        sentence_annotation = SentenceAnnotation(sentence=sentence, number=index, parse=line)
                    sentence_annotation.save()

                if len(question.sentences.all()) - 1 == sentence.index:
                    pk_list = [q.pk for q in Question.objects.all()]
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

                return redirect(request.POST['next'])

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

class SemanticParseListView(QuestionListView):
    template_name = 'semantics/semanticparse_list.html'


class ChoiceAnnotateView(View):
    def get(self, request, question_pk, choice_number):
        question = Question.objects.get(pk=question_pk)
        choice = Choice.objects.get(question=question, number=choice_number)
        if ChoiceAnnotation.objects.filter(choice=choice).exists():
            annotation_text = ChoiceAnnotation.objects.get(choice=choice).text
        else:
            annotation_text = ""
        form = ChoiceAnnotationForm(initial={'text': annotation_text})
        data = {'choice': choice, 'form': form, 'next': ''}
        # TODO : create template
        return render(request, 'semantics/choiceannotation_annotate.html', data)

    def post(self, request, question_pk, choice_number):
        question = Question.objects.get(pk=question_pk)
        choice = Sentence.objects.get(question=question, number=choice_number)
        form = SentenceParseForm(request.POST)
        if form.is_valid():
            lines = form.cleaned_data['text'].split('\r\n')
            valid = True
            if len(lines) > 1:
                valid = False

            if valid:
                line = lines[0]
                line = line.rstrip().lstrip()
                if ChoiceAnnotation.objects.filter(choice=choice).exists():
                    choice_annotation = ChoiceAnnotation.objects.get(choice=choice)
                    choice_annotation.text = line
                else:
                    choice_annotation = ChoiceAnnotation(choice=choice, text=line)
                choice_annotation.save()

                if len(question.choices.all()) - 1 == choice.number:
                    pk_list = [q.pk for q in Question.objects.all()]
                    next_question_pk = pk_list[pk_list.index(int(question_pk)) + 1]
                    next_choice_number = 0
                else:
                    next_question_pk = question_pk
                    next_choice_number = "%d" % (int(choice_number) + 1)

                kwargs = {'question_pk': next_question_pk, 'choice_number': next_choice_number}
                data = {'title': 'Success',
                        'message': 'Choice annotated successfully.',
                        'link': reverse('semantics-choice-annotate', kwargs=kwargs),
                        'linkdes': 'Annotate the next choice.'}
                return render(request, 'result.html', data)

        data = {'title': 'Failed',
                'message': "%r" % (invalid_lines),
                'linkdes': 'Go back and upload the tree again.'}
        return render(request, 'result.html', data)
