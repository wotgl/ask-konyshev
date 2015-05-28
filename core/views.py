from django.shortcuts import render
from django.http import Http404, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from core.models import Question, Profile, Tag, Answer, QLike, ALike
from core.forms import LoginForm, SignUpForm, handleUploadedFile, AskForm, AnswerForm
from core.forms import EditProfileForm, ChangePasswordForm, EditPhotoForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
from django.core.urlresolvers import reverse
from core.functions import pagination, nameParser, checkURL, collectLikes, sendMail
from django.db import IntegrityError
from django.core.validators import validate_email, ValidationError
from django.contrib.auth.hashers import check_password
import json
from django.template.context_processors import csrf
from django.views.decorators.http import require_http_methods, require_POST
from django.contrib.auth.decorators import login_required
import memcache
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
import urllib2
import requests # $ pip install requests
import json
from itertools import chain

N = 10  # Number of questions on page
number_of_answers = 10   # Number of answers on question page


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

    # Likes here
    context['likes'] = collectLikes(request, question_list)

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
    context['likes'] = collectLikes(request, answer_list)
    context['Qlikes'] = collectLikes(request, [question])

    if question.author == request.user:
        context['author'] = True
    else:
        context['author'] = False
    
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


@require_POST
@login_required(login_url='/login/')
def new_answer(request):
    context = {}

    # if request.user.is_authenticated():
    form = AnswerForm(request.POST, request=request or None)

    if form.is_valid():
        page_id = request.POST.get('page_id')
        question_id = request.POST.get('question_id')
        count = request.POST.get('count')
        question = Question.objects.get(id=question_id)

        answer = form.save(question)

        # Check 'next page'
        # if new answer go to new page => page_id++
        count = int(count)
        if count % number_of_answers == 0 and not count == 0:
            page_id = int(page_id)
            page_id = page_id + 1

        json_data = json.dumps({'new_answer': {'id': answer.id, 
        'text': answer.text, 
        'author': answer.author.username, 
        'rating': answer.rating,
        'filename': str(answer.author.profile.filename),
        'url': 'http://127.0.0.1/question/' + str(question_id),
        'page_id': page_id}
        })

        requests.post('http://127.0.0.1:8888/', data=json_data)

        # helpLink = 'http://127.0.0.1/question/' + str(question_id) + '?page=' + str(page_id) + '#' + str(answer.id)
        # sendMail(question.author.email, question, answer, helpLink)
        # Redirect to answer
        return HttpResponsePermanentRedirect(reverse("question", kwargs={"question_id": question_id}) 
            + "?page=" + str(page_id) + "#" + str(answer.id))
    else:
        return HttpResponseRedirect(reverse("question", kwargs={"question_id": request.POST.get('question_id')}))


def tag(request, tag_name): 
    try:
        tag_list = Tag.objects.get(name=tag_name)
    except Tag.DoesNotExist, e:
        raise Http404

    question_list = tag_list.question_set.order_by('-date').all()

    # Create Paginator
    question_list = pagination(request, question_list, N)

    context = {'question_list': question_list, 'tag_name': tag_name}
    context['likes'] = collectLikes(request, question_list)
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

                return HttpResponseRedirect(reverse("index"))       # Return to index page

            # Return initial form
            context['form'] = form

        return render(request, 'signup.html', context)      # return this page with error message

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
                    if user.is_active:      # may be banned?
                        login(request, user)
                        url = request.POST.get('next')

                        return HttpResponseRedirect(url)        # 302 Redirect
                    else:
                        context['form'] = {'message': 'Account is disable :c'}  # Return a disable account
                else:
                    # Return an invalid login error message
                    context['form'] = form
                    context['next'] = request.POST.get('next')
                    context['message'] = {'message': 'Unable to login'}

        if request.method == 'GET':
            url = request.GET.get('next')
            if url:
                context['next'] = url
            else:
                context['next'] = request.META['HTTP_REFERER']

        return render(request, 'login.html', context)
    else:
        return HttpResponseRedirect(reverse("index"))       # 302
    

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def base(request):
    return render(request, 'base.html')


@login_required(login_url='/login/')
def ask(request):
    context = {'form': AskForm}
    if request.method == "POST":
        form = AskForm(request.POST, request=request or None)

        if form.is_valid():
            question = form.save()
            return HttpResponseRedirect('/question/' + str(question.id))
        context['form'] = form

    return render(request, 'ask.html', context)


@login_required(login_url='/login/')
def settings(request):
    context = {'form_edit': EditProfileForm, 'form_photo': EditPhotoForm, 'form_password': ChangePasswordForm}

    return render(request, 'settings.html', context)


@login_required(login_url='/login/')
def edit_profile(request):
    context = {'form_edit': EditProfileForm, 'form_photo': EditPhotoForm, 'form_password': ChangePasswordForm}

    if request.method == "POST":
        form = EditProfileForm(request.POST, request=request or None)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('settings'))
        
        context['form_edit'] = form
        return render(request, 'settings.html', context)

    return HttpResponseRedirect(reverse('settings'))
            

@login_required(login_url='/login/')         
def change_password(request):
    context = {'form_edit': EditProfileForm, 'form_photo': EditPhotoForm, 'form_password': ChangePasswordForm}

    if request.method == "POST":
        form = ChangePasswordForm(request.POST, request=request or None)

        if form.is_valid():
            user = form.save()
            user = authenticate(username=user.username, password=form.cleaned_data['new_password'])
            login(request, user)
            return HttpResponseRedirect(reverse('settings'))
                
        context['form_password'] = form
        return render(request, 'settings.html', context)    

    return HttpResponseRedirect(reverse('settings'))


@login_required(login_url='/login/')  
def edit_photo(request):
    context = {'form_edit': EditProfileForm, 'form_photo': EditPhotoForm, 'form_password': ChangePasswordForm}

    if request.method == "POST":
        form = EditPhotoForm(request.POST, request.FILES, request=request)

        if form.is_valid():
            form.save()
        context['form_photo'] = form
        return render(request, 'settings.html', context)

    return HttpResponseRedirect(reverse('settings'))


@login_required(login_url='/login/')
def profile(request, username):
    try:
        user_profile = User.objects.get(username=username)
    except User.DoesNotExist, e:
        raise Http404

    context = {'user_profile': user_profile}
    return render(request, 'profile.html', context)


@login_required
@require_POST
def like(request):
    state = request.POST.get('state')
    button = request.POST.get('button')

    likeType = button.split('_')[0];

     # Parse value
    if state == 'like':
        value = 1
    elif state == 'dislike':
        value = -1
    else:
        return JsonResp('error')


    # Here code for question/answer
    if likeType == 'QlikeBtn' or likeType == 'QdislikeBtn':
        question_id = button.split('_')[1]    # Get id

        try:
            question = Question.objects.get(id=question_id)
        except Question.DoesNotExist, e:
            return JsonResp('error')

        try:
            state = question.likes.get(author=request.user)
            exist = True
            # return JsonResp('value exist')
        except QLike.DoesNotExist, e:
            exist = False

        # Many tap likes
        if exist:
            state.value = value
            state.save()
        else:
            question.likes.add(QLike.objects.create(author=request.user, value=value))

        likes = question.likes.all()
        rating = 0
        for like in likes:
            rating = rating + like.value

        question.rating = rating
        question.save()

        # One tap likes
        # if not exist:
        #     question.likes.add(QLike.objects.create(author=user, value=value))
        #     question.rating = question.rating + value
        #     question.save()

        return JsonResp(question.rating)
    elif likeType == 'AlikeBtn' or likeType == 'AdislikeBtn':
        answer_id = button.split('_')[1]    # Get id

        try:
            answer = Answer.objects.get(id=answer_id)
        except Answer.DoesNotExist, e:
            print 'YES!'
            return JsonResp('error')

        try:
            state = answer.likes.get(author=request.user)
            exist = True
            # return JsonResp('value exist')
        except ALike.DoesNotExist, e:
            exist = False


        # Many tap likes
        if exist:
            state.value = value
            state.save()
        else:
            answer.likes.add(ALike.objects.create(author=request.user, value=value))

        likes = answer.likes.all()
        rating = 0
        for like in likes:
            rating = rating + like.value

        answer.rating = rating
        answer.save()

        # One tap likes
        # if not exist:
        #     answer.likes.add(ALike.objects.create(author=user, value=value))
        #     answer.rating = answer.rating + value
        #     answer.save()
        
        return JsonResp(answer.rating)
    else:
        return JsonResp('error')

@login_required
@require_POST
def correct_answer(request):  
    data = request.POST.get('correct_id')
    correct_id = data.split('_')[1];

    try:
        answer = Answer.objects.get(id=correct_id)
        question = answer.question
    except Answer.DoesNotExist, e:
        return JsonResp('error')

    if question.author == request.user:
        if question.correct_answer == 0:
            question.correct_answer = correct_id
            answer.correct_answer = True
            question.save()
            answer.save()
            return JsonResp('OK')
        else:
            return JsonResp('value exist')
    else:
        return JsonResp('403')


def search(request):
    q = request.GET.get('q')

    q_list = Question.search.query(q)

    if len(q_list) == 0:
        raise Http404

    question_list = pagination(request, q_list, N) 

    context = {'question_list': question_list}

    # Likes here
    context['likes'] = collectLikes(request, question_list)

    context['q'] = q

    return render(request, 'search.html', context)


def JsonResp(answer):
    return HttpResponse(
        json.dumps(answer),
        content_type="application/json"
    )