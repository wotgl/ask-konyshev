from django.shortcuts import render
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from core.models import Question, Profile, Tag, Answer

N = 10	#Number of questions on page


def main(request):
	print request.path

	#	Switch path
	if request.path == '/':
		question_list = Question.objects.order_by('-date').all()
		html = 'index.html'
	elif request.path == '/popular/':
		question_list = Question.objects.order_by('-rating').all()
		html = 'popular.html'

	# Create Paginator
	question_list = pagination(request, question_list, N)

	# question_list = Question.objects.order_by('-date')[:N]
	context = {'question_list': question_list}
	return render(request, html, context)


#	check nubmer of question
def question(request, question_id):
	try:
		question = Question.objects.get(id=question_id)

		# Get answers list
		answer_list = question.answers.all()

		# Create Paginator
		answer_list = pagination(request, answer_list, 2)
		
		context = {'question': question, 'answer_list': answer_list}
		return render(request, 'question.html', context)
	except Exception, e:
		raise Http404("Question does not exist")

def tag(request, tag_name):
	question_list = []
	tag_list = Tag.objects.filter(name=tag_name).select_related('title')	#tag_list type = QuerySet
	for tag in tag_list:
		question = tag.question_set.all()	#question type = QuerySet
		for q in question:
			question_list.append(q)
		
	# Create Paginator
	question_list = pagination(request, question_list, N)

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
