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
    count_user = User.objects.latest('id').id
    count_profile = User.objects.latest('id').id

    with open('core/management/csv/user.csv', 'w') as csvfile:
        fieldnames = ['id', 'password', 'last_login', 'is_superuser', 'username', 'first_name', 
        'last_name', 'email', 'is_staff', 'is_active', 'date_joined']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for i in range(0, count):
            count_user = count_user + 1
            id = count_user
            password = User.objects.make_random_password()
            last_login = createDate()
            is_superuser = 0
            username = 'user' + str(count_user)
            first_name = 'Agent'
            last_name = 'Smith' + str(count_user)
            email = 'email' + str(count_user)
            is_staff = 0
            is_active = 0
            date_joined = createDate()
           
            writer.writerow(
            {'id': id, 'password': password, 'last_login': last_login, 'is_superuser': is_superuser, 
            'username': username, 'first_name': first_name, 'last_name': last_name, 'email': email, 
            'is_staff': is_staff, 'is_active': is_active, 'date_joined': date_joined}
            )

    with open('core/management/csv/profile.csv', 'w') as csvfile:
        fieldnames = ['id', 'rating', 'avatar', 'filename', 'user_id']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for i in range(0, count):
            count_profile = count_profile + 1
            id = count_profile
            rating = random.randint(0, 30)
            avatar = 0
            filename = 0
            user_id = count_profile
            writer.writerow(
            {'id': id, 'rating': rating, 'avatar': avatar, 'filename': filename, 'user_id': user_id}
            )


#   LOAD DATA INFILE 'answer.csv' INTO TABLE core_answer FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;
#   LOAD DATA INFILE 'question_answers.csv' INTO TABLE core_question_answers FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;

def createAnswer(count):
    count = int(count)
    print 'start createAnswer(%d)' %count

    count_answer = Answer.objects.latest('id').id
    count_question_answer = Answer.objects.latest('id').id
    count_question = Question.objects.latest('id').id
    temp_question = Question.objects.latest('id').id    #for question_answers.csv
    count_profile = User.objects.latest('id').id

    with open('core/management/csv/answer.csv', 'w') as csvfile:
        fieldnames = ['id', 'text', 'date', 'rating', 
        'correct_answer', 'author_id']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for i in range(0, count):
            count_answer = count_answer + 1
            id = count_answer
            text = 'answer#' + str(count_answer)
            date = createDate()
            rating = random.randint(0, 10)
            correct_answer = 0
            author_id = random.randint(0, count_profile)

            writer.writerow(
            {'id': id, 'text': text, 'date': date, 'rating': rating, 'correct_answer': correct_answer, 'author_id': author_id}
            )

    with open('core/management/csv/question_answers.csv', 'w') as csvfile:
        fieldnames = ['id', 'question_id', 'answer_id']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for i in range(0, count):
            count_question_answer = count_question_answer + 1
            id = count_question_answer
            question_id = random.randint(0, temp_question)
            answer_id = count_question_answer

            writer.writerow(
            {'id': id, 'question_id': question_id, 'answer_id': answer_id}
            )


#   LOAD DATA INFILE 'question.csv' INTO TABLE core_question FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;

def createQuestion(count):
    count = int(count)
    print 'start createQuestion(%d)' %count

    count_question = Question.objects.latest('id').id
    count_user = Profile.objects.latest('id').id

    with open('core/management/csv/question.csv', 'w') as csvfile:
        fieldnames = ['id', 'title', 'text', 'date', 
        'rating', 'author_id']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for i in range(0, count):
            count_question = count_question + 1
            id = count_question
            title = 'title#' + str(count_question)
            text = str(count_question) + 'text' * 20
            date = createDate()
            rating = random.randint(0, 20)
            author_id = random.randint(0, count_user)
             
            writer.writerow(
            {'id': id, 'title': title, 'text': text, 'date': date, 'rating': rating, 'author_id': author_id}
            )


#   LOAD DATA INFILE 'tag.csv' INTO TABLE core_tag FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;
#   LOAD DATA INFILE 'question_tags.csv' INTO TABLE core_question_tags FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;

def createTag(count):
    count = int(count)
    print 'start createQTag(%d)' %count

    count_tag = Tag.objects.latest('id').id
    count_question_tags = Tag.objects.latest('id').id
    count_question = Question.objects.latest('id').id

    with open('core/management/csv/tag.csv', 'w') as csvfile:
        fieldnames = ['id', 'name']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for i in range(0, count):
            count_tag = count_tag + 1
            id = count_tag
            name = 'tag#' + str(count_tag)
             
            writer.writerow(
            {'id': id, 'name': name}
            )

    with open('core/management/csv/question_tags.csv', 'w') as csvfile:
        fieldnames = ['id', 'question_id', 'tag_id']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for i in range(0, count):
            count_question_tags = count_question_tags + 1
            id = count_question_tags
            question_id = random.randint(0, count_question)
            tag_id = count_question_tags

            writer.writerow(
            {'id': id, 'question_id': question_id, 'tag_id': tag_id}
            )


#   main class & handler

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        if args[0] == 'Profile':
            createProfile(args[1])
        if args[0] == 'Answer':
            createAnswer(args[1])
        if args[0] == 'Question':
            createQuestion(args[1])
        if args[0] == 'Tag':
            createTag(args[1])

        

# struct of csv
# id,password,last_login,is_superuser,username,first_name,last_name,email,is_staff,is_active,date_joined
# 46,"pass",2015/04/12/10/10/10,0,"test514001","first","last","email",0,0,2015/04/12/10/10/10


            
