'''
Created on Jul 21, 2014

@author: minjoon

functions for updating the database
'''

from questions.models import QuestionTag, Question, Sentence, Choice, ChoiceWord, SentenceWord, SentenceExpression, \
    ChoiceExpression
from questions.views import _split_text
import geosolver.utils.prep as prep


def add_question(text, imgpath, tagwords=None):
    '''
    text: question text
    imgpath: path to the image
    '''
    if tagwords is None:
        tagwords = []

    question = Question(text=text,diagram=imgpath)
    question.save()

    for tagword in tagwords:
        if QuestionTag.objects.filter(word=tagword).exists():
            tag = QuestionTag.objects.get(word=tagword)
        else:
            tag = QuestionTag(word=tagword)
            tag.save()
        question.tags.add(tag)

    # Update new tags
    question.save()


def add_choice_words():
    choices = Choice.objects.filter(question__pk=1352)
    choice_words = ChoiceWord.objects.all()
    print(len(choice_words))
    for choice_word in choice_words:
        choice_word.delete()
    print("all choice words deleted")
    for choice in choices:
        words = sentence_to_words(choice.text)
        print(choice)
        for idx, word in words.iteritems():
            choice_word = ChoiceWord(text=word, index=idx, choice=choice)
            choice_word.save()

def delete_all():
    for choice_expression in ChoiceExpression.objects.all():
        choice_expression.delete()
    for sentence_expression in SentenceExpression.objects.all():
        sentence_expression.delete()
    for choice_word in ChoiceWord.objects.all():
        choice_word.delete()
    for sentence_word in SentenceWord.objects.all():
        sentence_word.delete()
    for sentence in Sentence.objects.all():
        sentence.delete()



def populate_choice_words():
    for choice in Choice.objects.all():
        words, statements, values = prep.sentence_to_words_statements_values(choice.text)
        for index, word in words.iteritems():
            sentence_word = ChoiceWord(choice=choice, index=index, text=word)
            sentence_word.save()
        for key, expr in statements.iteritems():
            sentence_expression = ChoiceExpression(choice=choice, index=key, text=expr)
            sentence_expression.save()
        for key, expr in values.iteritems():
            sentence_expression = ChoiceExpression(choice=choice, index=key, text=expr)
            sentence_expression.save()

def populate_sentences():
    for question in Question.objects.all():
        sentences = prep.paragraph_to_sentences(question.text)
        for index, text in sentences.iteritems():
            sentence = Sentence(index=index, text=text, question=question)
            sentence.save()

def populate_sentence_words():
    for sentence in Sentence.objects.all():
        words, statements, values = prep.sentence_to_words_statements_values(sentence.text)
        for index, word in words.iteritems():
            sentence_word = SentenceWord(sentence=sentence, index=index, text=word)
            sentence_word.save()
        for key, expr in statements.iteritems():
            sentence_expression = SentenceExpression(sentence=sentence, index=key, text=expr)
            sentence_expression.save()
        for key, expr in values.iteritems():
            sentence_expression = SentenceExpression(sentence=sentence, index=key, text=expr)
            sentence_expression.save()

def do_all():
    delete_all()
    populate_sentences()
    populate_choice_words()
    populate_sentence_words()
