#   How to use
#   python manage.py generate Profile [count]
#   cd core/management/csv/
#   transfer files to MySQL dir
#   use your_database_name;
#   upload data

from django.core.management.base import BaseCommand, CommandError
from core.models import Profile, Answer, Question, Tag
from django.contrib.auth.models import User
import random
import csv

def createDate():
    year = random.randint(2013, 2015)
    month = random.randint(1, 12)
    day = random.randint(1, 30)
    hour = random.randint(0, 23)
    minutes = random.randint(0, 59)
    seconds = random.randint(0, 59)

    answer = str(year) + '/' + str(month) + '/' + str(day) + '/' + str(hour) + '/' + str(minutes) + '/' + str(seconds)

    return answer


#   LOAD DATA INFILE 'user.csv' INTO TABLE auth_user FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;
#   LOAD DATA INFILE 'profile.csv' INTO TABLE core_profile FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;

def createProfile(count):
    count = int(count)
    print 'start createProfile(%d)' %count

    #count_user = User.objects.count()
    count_user = User.objects.count()

    for i in range(0, count):
        count_user = count_user + 1
        username = 'user' + str(count_user)
        email = 'email' + str(count_user)
        password = 'pass' + str(count_user)
        user = User.objects.create_user(username, email, password)

        user.first_name = 'Agent'
        user.last_name = 'Smith' + str(count_user)
        user.save()

        rating = random.randint(0, 10)
        filename_id = random.randint(0,10)      #in dir uploads 0..10 jpg avatars
        filename = str(filename_id) + '.jpg'
        Profile.objects.create(user=user, rating=rating, filename=filename)


#   LOAD DATA INFILE 'answer.csv' INTO TABLE core_answer FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;
#   LOAD DATA INFILE 'question_answers.csv' INTO TABLE core_question_answers FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;

def createAnswer():
    
    count_answer = Answer.objects.count()
    count_user = Profile.objects.count()

    count_answer = count_answer + 1

    text = str(count_answer) + '_text_answer' * 5
    author_id = random.randint(0, count_user)
    author = Profile.objects.get(id=author_id)
    rating = random.randint(0, 10)

    a = Answer.objects.create(text=text, author=author, rating=rating)
    return a
        


#   LOAD DATA INFILE 'question.csv' INTO TABLE core_question FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;

def createQuestion(count):
    count = int(count)
    print 'start createQuestion(%d)' %count

    count_question = Question.objects.count()
    count_user = Profile.objects.count()

    for i in range(0, count):
        count_question = count_question + 1
        title = 'title' + str(count_question)
        text = str(count_question) + '_text' * 10
        author_id = random.randint(0, count_user)
        author = Profile.objects.get(id=author_id)
        rating = random.randint(0, 10)
        q = Question.objects.create(title=title, text=text, author=author, rating=rating)

        for i in range(0, random.randint(0, 5)):
            q.answers.add(createAnswer())

        for i in range(0, random.randint(0, 5)):
            q.tags.add(createTag())

        q.save()


#   LOAD DATA INFILE 'tag.csv' INTO TABLE core_tag FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;
#   LOAD DATA INFILE 'question_tags.csv' INTO TABLE core_question_tags FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;

def createTag():
   
    count_tag = Tag.objects.count()

    
    count_tag = count_tag + 1
    name = 'tag#' + str(count_tag)

    t = Tag.objects.create(name=name)
    return t


#   main class & handler

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        if args[0] == 'Profile':
            createProfile(args[1])
        if args[0] == 'Question':
            createQuestion(args[1])


        

# struct of csv
# id,password,last_login,is_superuser,username,first_name,last_name,email,is_staff,is_active,date_joined
# 46,"pass",2015/04/12/10/10/10,0,"test514001","first","last","email",0,0,2015/04/12/10/10/10


            
