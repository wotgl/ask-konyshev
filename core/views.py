from django.shortcuts import render
from django.shortcuts import render_to_response

def index(request):
	return render(request, 'index.html')

def signup(request):
	return render(request, 'signup.html')

def login(request):
	return render(request, 'login.html')

def base(request):
    #render(request, '/html/base.html')
    return render(request, 'base.html')

def question(request):
    return render(request, 'question.html')

def ask(request):
    return render(request, 'ask.html')
