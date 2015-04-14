from django.shortcuts import render
from core.models import Question, Profile, Tag, Answer

N = 10	#Number of questions on page

def index(request):
	question_list = Question.objects.order_by('-date')[:N]
	context = {'question_list': question_list}
	return render(request, 'index.html', context)

def popular(request):
	question_list = Question.objects.order_by('-rating')[:N]
	context = {'question_list': question_list}
	return render(request, 'popular.html', context)

#	check nubmer of question
def question(request, question_id):
	question = Question.objects.get(id=question_id)

	context = {'question': question}
	return render(request, 'question.html', context)

def tag(request, tag_name):
	question_list = []
	tag_list = Tag.objects.filter(name=tag_name).select_related('title')	#tag_list type = QuerySet
	for tag in tag_list:
		question = tag.question_set.all()	#question type = QuerySet
		for q in question:
			question_list.append(q)
		
	context = {'question_list': question_list, 'tag_name': tag_name}
	return render(request, 'tag.html', context)




def signup(request):
	return render(request, 'signup.html')

def login(request):
	return render(request, 'login.html')

def base(request):
    return render(request, 'base.html')

def ask(request):
    return render(request, 'ask.html')
