from django.shortcuts import render
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from core.models import Question, Profile, Tag, Answer
from core.forms import LoginForm, SignUpForm, handleUploadedFile, AskForm, AnswerForm
from core.forms import EditProfileForm, ChangePasswordForm, EditPhotoForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
from django.core.urlresolvers import reverse
from core.functions import pagination, nameParser, checkURL
from django.db import IntegrityError
from django.core.validators import validate_email, ValidationError
from django.contrib.auth.hashers import check_password

N = 10	# Number of questions on page
number_of_answers = 10	 # Number of answers on question page


def main(request):
	# Switch path
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


# check nubmer of question
def question(request, question_id):

	try:
		question = Question.objects.get(id=question_id)
	except Question.DoesNotExist, e:
		raise Http404

	# Get answers list
	answer_list = question.answer_set.all()

	# Create Paginator
	answer_list = pagination(request, answer_list, number_of_answers)
	
	context = {'question': question, 'answer_list': answer_list}

	
	'''
	Get AnswerForm
	set help values int HTML "question.html": question_id, page_id
	where the latter is calculated as: 
		answer_list(Page object)
		answer_list.paginator(Paginator object)
		answer_list.paginator.num_pages(count of num_pages)
	'''
	form = AnswerForm
	context['form'] = form

	return render(request, 'question.html', context)


def new_answer(request):
	context = {}

	if request.user.is_authenticated():
		if request.method == "POST":
			form = AnswerForm(request.POST or None)

			if form.is_valid():
				text = form.cleaned_data['text']
				page_id = request.POST.get('page_id')
				question_id = request.POST.get('question_id')
				count = request.POST.get('count')

				author = User.objects.get(username=request.user)
				question = Question.objects.get(id=question_id)

				answer = Answer.objects.create(text=text, author=author, question=question)
 

				# Check 'next page'
				# if new answer go to new page => page_id++
				count = int(count)
				if count % number_of_answers == 0 and not count == 0:
					page_id = int(page_id)
					page_id = page_id + 1

				# Redirect to answer
				return HttpResponsePermanentRedirect(reverse("question", kwargs={"question_id": question_id}) 
					+ "?page=" + str(page_id) + "#" + str(answer.id))
			else:
				return HttpResponseRedirect(reverse("question", kwargs={"question_id": request.POST.get('question_id')}))

	return HttpResponseRedirect(reverse('question', kwargs={"question_id": request.POST.get('question_id')}))


def tag(request, tag_name):	

	# 404 not cool

	try:
		tag_list = Tag.objects.get(name=tag_name)
	except Tag.DoesNotExist, e:
		raise Http404

	
	question_list = tag_list.question_set.order_by('-date').all()

	# Create Paginator
	question_list = pagination(request, question_list, N)

	context = {'question_list': question_list, 'tag_name': tag_name}
	return render(request, 'tag.html', context)


def signup(request):
	context = {'form': SignUpForm}

	# Check for auth
	if not request.user.is_authenticated():
		if request.method == "POST":
			form = SignUpForm(request.POST, request.FILES)

			if form.is_valid():
				user = form.save()
				
        		# Login new user
				user = authenticate(username=user.username, password=form.cleaned_data['password'])
				login(request, user)

				return HttpResponseRedirect(reverse("index"))		# Return to index page

			# Return initial form
			context['form'] = form

		return render(request, 'signup.html', context)		# return this page with error message

	# If user is authenticated	
	return HttpResponseRedirect(reverse("index"))


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
					if user.is_active:		# may be banned?
						login(request, user)
						url = request.GET.get('continue')				# Back where you came from

						return HttpResponseRedirect(url)		# 302 Redirect
					else:
						context['form'] = {'message': 'Account is disable :c'}	# Return a disable account
				else:
					# Return an invalid login error message
					form.set_initial(username)
					context['form'] = form
					context['message'] = {'message': 'Unable to login'}

		# Try get HTTP_REFERER
		try:
			context['continue'] = request.META['HTTP_REFERER']
		except Exception, e:
			context['continue'] = '/'

		return render(request, 'login.html', context)
	else:
		return HttpResponseRedirect(reverse("index"))		# 302
	

def logout_view(request):
	logout(request)
	return HttpResponseRedirect(reverse('index'))


def base(request):
    return render(request, 'base.html')


def ask(request):
	context = {'form': AskForm}

	if request.user.is_authenticated():
		if request.method == "POST":
			form = AskForm(request.POST or None)

			if form.is_valid():
				title = form.cleaned_data['title']
				text = form.cleaned_data['text']
				tags = form.cleaned_data['tags']

				author = User.objects.get(username=request.user)
				question = Question.objects.create(title=title, text=text, author=author)

				tag_list = tags.split(' ')
				for tag in tag_list:
					t = Tag.objects.get_or_create(name=tag)
					question.tags.add(t[0])

				return HttpResponseRedirect('/question/' + str(question.id))
			else:
				context['message'] = {'message': 'Invalid fields'}
				context['form'] = form
	else:
		return HttpResponseRedirect(reverse('login'))
		# context['message'] = {'message': '<a href="/login">Login</a> or <a href="/signup">sign up</a> to ask'}

	return render(request, 'ask.html', context)


def settings(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse("index"))

	context = {'form_edit': EditProfileForm, 'form_photo': EditPhotoForm, 'form_password': ChangePasswordForm}

	return render(request, 'settings.html', context)


def edit_profile(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse("index"))

	context = {'form_edit': EditProfileForm, 'form_photo': EditPhotoForm, 'form_password': ChangePasswordForm}

	if request.method == "POST":
		form = EditProfileForm(request.POST or None)

		if form.is_valid():
			first_name = form.cleaned_data['first_name']
			last_name = form.cleaned_data['last_name']
			try:
				user = User.objects.get(username=request.user)
			except User.DoesNotExist, e:
				return Http404

			if first_name:
				user.first_name = first_name
			if last_name:
				user.last_name = last_name

			user.save()
		else:
			context['message_profile'] = {'message': 'Invalid fields'}
		
		return render(request, 'settings.html', context)

	return HttpResponseRedirect(reverse('settings'))
			
			
def change_password(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse("index"))

	context = {'form_edit': EditProfileForm, 'form_photo': EditPhotoForm, 'form_password': ChangePasswordForm}

	if request.method == "POST":
		form = ChangePasswordForm(request.POST or None)

		if form.is_valid():
			password = form.cleaned_data['password']
			new_password = form.cleaned_data['new_password']
			repeat_new_password = form.cleaned_data['repeat_new_password']

			try:
				user = User.objects.get(username=request.user)
			except User.DoesNotExist, e:
				return Http404

			if check_password(password, user.password):
				if new_password == repeat_new_password:
					user.set_password(new_password)
					user.save()

					user = authenticate(username=user.username, password=new_password)
					login(request, user)

					return HttpResponseRedirect(reverse('settings'))
				else:
					context['message_pass'] = {'message': 'Passwords do not match'}
			else:
				context['message_pass'] = {'message': 'Wrong password'}
			
		context['message_pass'] = {'message': 'Invalid fields'}
		
		return render(request, 'settings.html', context)


	return HttpResponseRedirect(reverse('settings'))
	
		
def edit_photo(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse("index"))

	context = {'form_edit': EditProfileForm, 'form_photo': EditPhotoForm, 'form_password': ChangePasswordForm}

	if request.method == "POST":
		form = EditPhotoForm(request.POST, request.FILES)

		if form.is_valid():
			valid = True

			
			filename = handleUploadedFile(request.FILES['pic'])		# Upload file

			
			# Check size of file if file = True
			if valid and filename:
				try:
					form.check_pic()
					valid = True
				except ValidationError, e:
					valid = False
					context['message_pic'] = {'message': 'This file too large'}

			if valid:
				try:
					user = User.objects.get(username=request.user)
				except User.DoesNotExist, e:
					return Http404
				
				user.profile.filename = filename

				user.save()
				user.profile.save()
		else:
			context['message_pic'] = {'message': 'Invalid fields'}
		return render(request, 'settings.html', context)

	return HttpResponseRedirect(reverse('settings'))
			

def profile(request, username):
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse('login'))

	try:
		user_profile = User.objects.get(username=username)
	except User.DoesNotExist, e:
		raise Http404

	context = {'user_profile': user_profile}
	return render(request, 'profile.html', context)
