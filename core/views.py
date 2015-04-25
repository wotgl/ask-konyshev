from django.shortcuts import render
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from core.models import Question, Profile, Tag, Answer
from core.forms import LoginForm, SignUpForm, handleUploadedFile
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponsePermanentRedirect
from django.core.urlresolvers import reverse
from core.functions import pagination, nameParser, checkURL
from django.db import IntegrityError
from django.core.validators import validate_email, ValidationError

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
	number_of_answers = 5
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


#	Add check file
def signup(request):
	context = {'form': SignUpForm}

	#	Check for auth
	if not request.user.is_authenticated():
		if request.method == "POST":
			form = SignUpForm(request.POST, request.FILES)


			if form.is_valid():
				#	SignUp code here
				valid = True 	#Valid to SignUp


				username = form.cleaned_data['username']
				email = form.cleaned_data['email']
				password = form.cleaned_data['password']
				filename = form.cleaned_data['pic']				


				#	Check file existence		
				if request.FILES:
					filename = handleUploadedFile(request.FILES['pic'])		#	Upload file
				

				#	Check size of file
				if valid:
					try:
						form.check_pic()

						valid = True
					except ValidationError, e:
						valid = False
						context['message'] = {'message': 'This file too large'}


				#	Check email for validity 
				if valid:
					try:
						validate_email(email)

						valid = True
					except ValidationError, e:
						valid = False
						context['message'] = {'message': 'This email not valid'}


				#	Check email existence
				if valid:
					try:
						User.objects.get(email=email)

						valid = False
						context['message'] = {'message': 'This email is already exist'}
					except User.DoesNotExist, e:
						valid = True
					

				#	If all checks True => try to create the user 
				if valid:
					try:
						user = User.objects.create_user(username, email, password)

						if filename:
					        	Profile.objects.create(user=user, filename=filename)
					        else:
					        	Profile.objects.create(user=user)

		        		#	Login new user
						user = authenticate(username=username, password=password)
						login(request, user)

						return HttpResponsePermanentRedirect(reverse("index"))		#	Return to index page
					except IntegrityError, e:
						context['message'] = {'message': 'This username is already exist'}


			#	If bad fields: form is not valid
			else:
				context['message'] = {'message': 'Invalid fields'}
			

			#	Return initial form
			context['form'] = form

		return render(request, 'signup.html', context)		#	return this page with error message

	#	If user is authenticated	
	return HttpResponsePermanentRedirect(reverse("index"))



def login_view(request):
	context = {'form': LoginForm}

	if not request.user.is_authenticated():
		if request.method == "POST":
			form = LoginForm(request.POST or None)

			if form.is_valid():
				username = form.cleaned_data['username']
				password = form.cleaned_data['password']

				user = authenticate(username=username, password=password)

				if user is not None:
					if user.is_active:		#	may be banned?
						login(request, user)
						url = request.GET.get('continue')				#	Back where you came from

						return HttpResponsePermanentRedirect(url)		#	302 Redirect
					else:
						#	Return a disable account
						context['form'] = {'message': 'Account is disable :c'}
				else:
					#	Return an invalid login error message
					form.set_initial(username)
					context['form'] = form
					context['message'] = {'message': 'We could not find an account for that username'}

		#	Try get HTTP_REFERER
		try:
			context['continue'] = request.META['HTTP_REFERER']
		except Exception, e:
			context['continue'] = '/'

		return render(request, 'login.html', context)
	else:
		return HttpResponsePermanentRedirect(reverse("index"))		#	302
	
def logout_view(request):
	logout(request)
	return HttpResponsePermanentRedirect(reverse("index"))


def base(request):
    return render(request, 'base.html')

def ask(request):
    return render(request, 'ask.html')





