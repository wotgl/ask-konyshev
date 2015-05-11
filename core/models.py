from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

#   Profile with User from django.contrib.auth.models;
#   User include username, email, first_name, last_name, password etc
class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    # filename = models.CharField(max_length=50, default='default.png')
    filename = models.ImageField(upload_to='/uploads/', default='default.png')

    def __unicode__(self):
        return str(self.user.username)


class Tag(models.Model):
    name = models.CharField(max_length=140)

    def __unicode__(self):
        return str(self.name)


#   Table of like questions
class QLike(models.Model):
    author = models.ForeignKey(User)
    value = models.IntegerField(default=0)


class Question(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    author = models.ForeignKey(User)
    date = models.DateTimeField(default=datetime.now)
    rating = models.IntegerField(db_index=True, default=0)
    tags = models.ManyToManyField(Tag)
    likes = models.ManyToManyField(QLike)
    correct_answer = models.IntegerField(default=0)

    def __unicode__(self):
        return str(self.title)


#   Table of like answers
class ALike(models.Model):
    author = models.ForeignKey(User)
    value = models.IntegerField(default=0)


class Answer(models.Model):
    text = models.TextField()
    author = models.ForeignKey(User)
    date = models.DateTimeField(default=datetime.now)
    rating = models.IntegerField(default=0)
    correct_answer = models.BooleanField(default=False)
    question = models.ForeignKey(Question)
    likes = models.ManyToManyField(ALike)

    def __unicode__(self):
        return str(self.text)
