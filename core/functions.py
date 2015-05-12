from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404, HttpResponse
from core.models import Question, Profile, Tag, Answer, QLike, ALike
from django.contrib.auth.models import User
# from django.core.mail import send_mail
from django.core.mail import send_mail as core_send_mail
from django.core.mail import EmailMultiAlternatives
import threading


# Help Functions

def pagination(request, list, number_of_page):
    paginator = Paginator(list, number_of_page) # Show number_of_page contacts per page
    page = request.GET.get('page')

    try:
        list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        raise Http404('Not found')

    return list


# Name parser

def nameParser(name):
    parse = name.split(' ')
    dict = {'first_name': parse[0], 'last_name': parse[1:]}
    last_name = ' '.join(dict['last_name'])     # list to string
    dict['last_name'] = last_name

    return dict

# For redirect

def checkURL(url):
    pattern = '127.0.0.1'
    if pattern in url:
        return True
    return False

def collectLikes(request, elements):
    likes = []
    if request.user.is_authenticated():
        for element in reversed(elements):
            try:
                like = element.likes.get(author=request.user)
                if like.value == 1:
                    likes.append(1)
                else:
                    likes.append(-1)
            except QLike.DoesNotExist, e:
                likes.append(0)
            except ALike.DoesNotExist, e:
                likes.append(0)   
    else:
        for i in elements:
            likes.append(0)
    return likes


# Mail

def sendMail(email, question, answer, link):
    subject = 'New answer to ' + str(question.title)
    message = 'Hey, ' + str(question.author.username) + '! ' + str(answer.author.username) + ' answered your question.' + ' Check it: ' + str(link)
    send_mail(subject, message, 'agentsupercat@gmail.com', [email], fail_silently=False)

class EmailThread(threading.Thread):
    def __init__(self, subject, body, from_email, recipient_list, fail_silently, html):
        self.subject = subject
        self.body = body
        self.recipient_list = recipient_list
        self.from_email = from_email
        self.fail_silently = fail_silently
        self.html = html
        threading.Thread.__init__(self)

    def run (self):
        msg = EmailMultiAlternatives(self.subject, self.body, self.from_email, self.recipient_list)
        if self.html:
            msg.attach_alternative(self.html, "text/html")
        msg.send(self.fail_silently)

def send_mail(subject, body, from_email, recipient_list, fail_silently=False, html=None, *args, **kwargs):
    EmailThread(subject, body, from_email, recipient_list, fail_silently, html).start()