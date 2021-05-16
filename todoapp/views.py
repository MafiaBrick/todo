from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login,logout,authenticate
# Create your views here.

def signup(request):
    if request.method == 'GET':
        return render (request, 'todoapp/signup.html', {'form':UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'],password  = request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('currenttodos')
            except IntegrityError:
                return render (request, 'todoapp/signup.html', {'form':UserCreationForm(),'error':'Данный пользователь уже существует в системе'})

        else:
            return render (request, 'todoapp/signup.html', {'form':UserCreationForm(),'error':'Пароли не совпадают'})
def currenttodos(request):
    return render(request,'todoapp/currenttodos.html')


def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

def home(request):
    return render(request, 'todoapp/home.html')

def loginuser(request):
    if request.method == 'GET':
        return render (request, 'todoapp/loginuser.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(request, username = request.POST['username'], password = request.POST['password'])
        if user is None:
            return render (request, 'todoapp/loginuser.html', {'form':AuthenticationForm(),'error':'Проверьте пароль и попробуйте еще раз'})
        else:
            login(request, user)
            return redirect('home')
