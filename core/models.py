from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    filename = models.CharField(max_length=50)

    def __unicode__(self):
        return str(self.user.username)


class Tag(models.Model):
    name = models.CharField(max_length=140)

    def __unicode__(self):
        return str(self.name)


#   Question Like
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

    def __unicode__(self):
        return str(self.title)


#   Answer Like
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
