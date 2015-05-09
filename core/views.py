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
from core.functions import pagination, nameParser, checkURL
from django.db import IntegrityError
from django.core.validators import validate_email, ValidationError
from django.contrib.auth.hashers import check_password
import json
from django.template.context_processors import csrf

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
                        url = request.GET.get('redirect')               # Back where you came from

                        return HttpResponseRedirect(url)        # 302 Redirect
                    else:
                        context['form'] = {'message': 'Account is disable :c'}  # Return a disable account
                else:
                    # Return an invalid login error message
                    context['form'] = form
                    context['next'] = request.POST.get('next')
                    context['message'] = {'message': 'Unable to login'}

        if request.method == 'GET':
            '''
                If user has true redirect e.g. /ask; /profile/<id>;
                    set context['next'] = redirect;
                else 
                    get HTTP_REFERER
            '''
            if not request.GET.get('redirect'):
                # Try get HTTP_REFERER
                try:
                    context['next'] = request.META['HTTP_REFERER']
                except Exception, e:
                    context['next'] = '/'   
            else:
                context['next'] = request.GET.get('redirect')


        return render(request, 'login.html', context)
    else:
        return HttpResponseRedirect(reverse("index"))       # 302
    

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
                question = form.save(request.user)

                return HttpResponseRedirect('/question/' + str(question.id))
            context['form'] = form
    else:
        # add redirect to /ask after login
        request.META['HTTP_REFERER'] = '/ask'
        return HttpResponseRedirect('/login?redirect=' + str(request.META['HTTP_REFERER']))

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
        form = EditProfileForm(request.POST, request=request or None)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('settings'))
        
        context['form_edit'] = form
        return render(request, 'settings.html', context)

    return HttpResponseRedirect(reverse('settings'))
            
            
def change_password(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse("index"))

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
    
        
def edit_photo(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse("index"))

    context = {'form_edit': EditProfileForm, 'form_photo': EditPhotoForm, 'form_password': ChangePasswordForm}

    if request.method == "POST":
        form = EditPhotoForm(request.POST, request.FILES, request=request)

        if form.is_valid():
            form.save()
        context['form_photo'] = form
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


def like(request):
    if request.method == 'POST':
        if not request.user.is_authenticated():
            return JsonResp('User is not authorized')

        user = request.user
        state = request.POST.get('buttonpressed')
        form = request.POST.get('form')
        question_id = form.split('=')[1]    # Get id

        # Parse value
        if state == 'like':
            value = 1
        elif state == 'dislike':
            value = -1
        else:
            return JsonResp('error')

        try:
            question = Question.objects.get(id=question_id)
        except Question.DoesNotExist, e:
            return JsonResp('error')

        try:
            state = question.likes.get(author=user)
            exist = True
        except QLike.DoesNotExist, e:
            exist = False

        if exist:
            question.rating = question.rating - state.value
            state.value = value
            state.save()
        else:
            question.likes.add(QLike.objects.create(author=user, value=value))
        
        question.rating = question.rating + value
        question.save()


        return JsonResp(question.rating)

    else:
        raise Http404

def JsonResp(answer):
    return HttpResponse(
        json.dumps(answer),
        content_type="application/json"
    )



def create_post(request):
    if request.method == 'POST':
        post_text = request.POST.get('the_post')
        question_id = request.POST.get('question_id')
        # request_csrf_token = request.META.get('HTTP_X_CSRFTOKEN', '')
        print question_id
        response_data = {}

        # post = Post(text=post_text, author=request.user)
        # post.save()

        response_data['result'] = 'Create post successful!'
        # response_data['postpk'] = post.pk
        # response_data['text'] = post.text
        # response_data['created'] = post.created.strftime('%B %d, %Y %I:%M %p')
        # response_data['author'] = post.author.username

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        raise Http404 