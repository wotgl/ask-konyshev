from django.shortcuts import render

def index(request):
	return render(request, 'index.html')

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
