from django.shortcuts import render
from core.models import Question, Profile

N = 10

def index(request):
	question_list = Question.objects.order_by('-date')[:N]
	return render(request, 'index.html', {'question_list': question_list})

def popular(request):
	#question_list = Question.objects.all()
	question_list = Question.objects.order_by('-rating')[:N]
	return render(request, 'popular.html', {'question_list': question_list})

def tag(request, tag_name):
	#question_list = Question.objects.all()
	try:
		question_list = Question.objects.order_by('-rating')[:N]
		context = {'question_list': question_list, 'tag_name': tag_name}
		return render(request, 'tag.html', context)
	except Exception, e:
		return 404



def signup(request):
	return render(request, 'signup.html')

def login(request):
	return render(request, 'login.html')

def base(request):
    return render(request, 'base.html')

def question(request):
    return render(request, 'question.html')

def ask(request):
    return render(request, 'ask.html')
