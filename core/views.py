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
	except Question.DoesNotExist, e:
		raise Http404
	

	# Get answers list
	answer_list = question.answer_set.all()

	# Create Paginator
	number_of_answers = 2
	answer_list = pagination(request, answer_list, number_of_answers)
	
	context = {'question': question, 'answer_list': answer_list}
	return render(request, 'question.html', context)

def tag(request, tag_name):	

	#	404 not cool

	try:
		tag_list = Tag.objects.get(name=tag_name)
	except Tag.DoesNotExist, e:
		raise Http404

	
	question_list = tag_list.question_set.all()

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
