from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


#   How-to-create:
#   user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword') 
#   Profile.objects.create(user=user, args)
#user = models.ForeignKey(User)
#first_name = models.CharField(max_length=30)
#last_name = models.CharField(max_length=30)
#email = models.EmailField()
#nickname = models.ForeignKey(User.username)

class Profile(models.Model):
    user = models.OneToOneField(User)
    rating = models.IntegerField(default=0)
    #avatar = models.ImageField()
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
    #answers = models.ForeignKey(Answer)
    tags = models.ManyToManyField(Tag)
    #tags = models.ForeignKey(Tag)

    def __unicode__(self):
        return str(self.title)





