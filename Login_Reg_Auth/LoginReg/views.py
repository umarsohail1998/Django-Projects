from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse, HttpResponseRedirect
from .forms import SignUpForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
# Create your views here.


def index(request):
    return render(request, 'enroll/index.html')


def sign_up(request):
    if request.user.is_authenticated():
        if request.method == "POST":
            fm = SignUpForm(request.POST)
            if fm.is_valid():
                messages.success(request, "Account Created successfully !!")
                fm.save()
        else:
            fm = SignUpForm()
        return render(request, 'enroll/signup.html', {'form': fm})
    return HttpResponseRedirect('/profle/')


def user_login(request):
    if not request.user.is_authenticated():
        if request.method =="POST":
            fm = AuthenticationForm(request=request, data= request.POST)
            if fm.is_valid():
                uname = fm.cleaned_data['username']
                upass = fm.cleaned_data['password']
                user =  authenticate(username = uname, password = upass)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Logges in Succesfully !!')
                    return HttpResponseRedirect('/profile/')
        else:
            fm =  AuthenticationForm()
        
        return render(request, 'enroll/login.html', {'form': fm})
    return HttpResponseRedirect('/profile/')


def user_profile(request):
    if request.user.is_authenticated:
        return render(request, 'enroll/profile.html', {'name': request.user})
    else:
        return HttpResponseRedirect('/login/')

def user_logout(request):
    # print("jello")
    # for x in range(100000):
    #     pass
    logout(request)
    return HttpResponseRedirect('/login/')

# def sign_up(request):
#     if request.method == "POST":
#         fm = UserCreationForm(request.POST)
#         if fm.is_valid():
#             fm.save()
#     else:
#         fm = UserCreationForm()
#     return render(request, 'enroll/signup.html', {'form': fm})