#   How to use
#   python manage.py generatev2 Profile [count]
#   python manage.py generatev2 Question [count]

from django.core.management.base import BaseCommand, CommandError
from core.models import Profile, Answer, Question, Tag, QLike, ALike
from django.contrib.auth.models import User
import random


def createProfile(count):
    count = int(count)
    print 'start createProfile(%d)' %count

    count_user = User.objects.count()

    for i in range(0, count):
        count_user = count_user + 1
        username = 'user' + str(count_user)
        email = 'email' + str(count_user)
        password = 'pass' + str(count_user)

        #   Create User
        user = User.objects.create_user(username, email, password)

        user.first_name = 'Agent'
        user.last_name = 'Smith' + str(count_user)
        user.save()

        #rating = random.randint(0, 10)
        filename_id = random.randint(0,10)      #In the directory '/uploads' must be '0.jpg'...'10.jpg' avatars
        filename = str(filename_id) + '.jpg'
        Profile.objects.create(user=user, filename=filename)


#   Create random answer

def createAnswer(q): 
    count_answer = Answer.objects.count()
    count_user = Profile.objects.count()

    count_answer = count_answer + 1

    text = 'text_answer' + str(count_answer)
    author_id = random.randint(1, count_user)
    author = Profile.objects.get(id=author_id)
    #rating = random.randint(-10, 20)

    a = Answer.objects.create(text=text, author=author, question=q)

    return a


#   Create random answer

def createTag():
    id_tag = random.randint(0, 20)
    name = 'tag' + str(id_tag)

    t = Tag.objects.get_or_create(name=name)

    return t[0]     #(<Tag: 12>, True)


#   Create random question

def createQuestion(count):
    count = int(count)
    print 'start createQuestion(%d)' %count

    count_question = Question.objects.count()
    count_user = Profile.objects.count()

    for i in range(0, count):
        count_question = count_question + 1
        title = 'title' + str(count_question)
        text = str(count_question) + '_text' * 10
        author_id = random.randint(1, count_user)
        try:
            author = Profile.objects.get(id=author_id)
        except Profile.DoesNotExist, e:
            break
        #rating = random.randint(0, 10)
        q = Question.objects.create(title=title, text=text, author=author)

        #   Add answers
        for i in range(0, random.randint(0, 10)):
           createAnswer(q)

        #   Add tags
        for i in range(0, random.randint(0, 5)):
            q.tags.add(createTag())

        q.save()

        #   Set likes to random questions and random answers from this author
        setLikes(random.randint(0, 20), author)



#   Set random likes

def setLikes(count, author):
    #   count = random
    count = int(count)
    print 'start setLikes(' + str(count) + ') from ' + str(author.user.username)

    count_question = Question.objects.count()
    count_answer = Answer.objects.count()

    #   Like for question
    for i in range(0, count):
        question_id = random.randint(1, count_question)
        question = Question.objects.get(id=question_id)
        likes = question.likes.all()

        #   Check for unique like
        f = True
        for like in likes:
            if like.author.user.id == author.id:
                f = False
                break

        if f:
            value = random.choice([-1, 1])
            question.likes.add(QLike.objects.create(author=author, value=value))
            question.rating = question.rating + value
            
            question.save()


    #   Like for answer
    for i in range(0, count):
        answer_id = random.randint(1, count_answer)
        answer = Answer.objects.get(id=answer_id)
        likes = answer.likes.all()


        #   Check for unique like
        f = True
        for like in likes:
            if like.author.user.id == author.id:
                f = False
                break

        if f:
            value = random.choice([-1, 1])
            answer.likes.add(ALike.objects.create(author=author, value=value))
            answer.rating = answer.rating + value
            
            answer.save()
        




#   main class & handler

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        if args[0] == 'Profile':
            createProfile(args[1])
        if args[0] == 'Question':
            createQuestion(args[1])