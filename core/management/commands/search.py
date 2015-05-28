#!/usr/bin/python
# -*- coding: utf-8 -*-

from core.models import Question, Answer
from django.core.management.base import BaseCommand, CommandError
import codecs

def createXML():
    f = codecs.open('search.xml', 'w', 'utf-8')

    # Border
    begin = '<?xml version="1.0" encoding="utf-8"?>\n\
<sphinx:docset xmlns:sphinx="http://sphinxsearch.com/">\n'
    end = '</sphinx:docset>'

    f.write(begin)

    questions = Question.objects.all()
    answers = Answer.objects.all()

    for question in questions:
        id = '<sphinx:document id="' + str(question.id) + '">\n'
        title = '\t<title>' + question.title + '</title>\n'
        Qtext = '\t<qtext>' + question.text + '</qtext>\n'
        Atext = ''

        for answer in answers:
            if answer.question.id == question.id:
                Atext = Atext + answer.text + ' '
        Atext = '\t<atext>' + Atext + '</atext>\n'

        data = id + title + Qtext + Atext + '</sphinx:document>\n'
        f.write(data)

    f.write(end)
    f.close()


class Command(BaseCommand):
    def handle(self, *args, **options):
        createXML()