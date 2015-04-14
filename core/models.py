from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class Profile(models.Model):
    user = models.OneToOneField(User)
    rating = models.IntegerField(default=0)
    filename = models.CharField(max_length=50)

    def __unicode__(self):
        return str(self.user.username)


class Answer(models.Model):
    text = models.TextField()
    author = models.ForeignKey(Profile)
    date = models.DateTimeField(default=datetime.now)
    rating = models.IntegerField(default=0)
    correct_answer = models.BooleanField(default=False)

    def __unicode__(self):
        return str(self.text)


class Tag(models.Model):
    name = models.CharField(max_length=140)

    def __unicode__(self):
        return str(self.name)


class Question(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    author = models.ForeignKey(Profile)
    date = models.DateTimeField(default=datetime.now)
    rating = models.IntegerField(default=0)
    answers = models.ManyToManyField(Answer)
    tags = models.ManyToManyField(Tag)

    def __unicode__(self):
        return str(self.title)





