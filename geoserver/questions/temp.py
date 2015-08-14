from questions.internal import reset_question
from questions.models import QuestionTag, Question, Choice

__author__ = 'minjoon'

def tag_questions():
    """
    tag questions with 1043 <= pk <= 1152

    :return:
    """
    tag = QuestionTag.objects.get(word="practice")
    questions = Question.objects.filter(pk__gte=1043, pk__lte=1152)
    for question in questions:
        question.tags.add(tag)

def remove_tag():
    emnlp = QuestionTag.objects.get(word='emnlp')
    practice = QuestionTag.objects.get(word='practice')
    for question in Question.objects.all():
        if practice in question.tags.all() and emnlp not in question.tags.all():
            question.tags.remove(practice)


def add_choices(question_pk, choice_words):
    """
    Aug 13, 2015
    Isaac's

    :return:
    """
    question = Question.objects.get(pk=question_pk)
    for index, choice_word in enumerate(choice_words):
        number = index+1
        choice = Choice(text=choice_word, number=number, question=question)
        choice.save()
    reset_question(question)