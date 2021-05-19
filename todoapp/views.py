from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login,logout,authenticate
from .forms import TodoForm
from .models import Todo
from django.views.generic.detail import DetailView
from django.utils import timezone
from django.contrib.auth.decorators import login_required
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


@login_required
def currenttodos(request):
    data = Todo.objects.filter(user = request.user,datecompleat__isnull = True).order_by('-date')
    return render(request,'todoapp/currenttodos.html',{'data':data})
@login_required
def compleatetodos(request):
    data = Todo.objects.filter(user = request.user,datecompleat__isnull = False)
    return render(request,'todoapp/compleatetodos.html',{'data':data})




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
@login_required
def addtodo(request):
    if request.method == 'GET':
        return render(request,'todoapp/addtodo.html',{'form':TodoForm()})
    else:
        try:
            infoForm = TodoForm(request.POST)
            newTodo = infoForm.save(commit=False)
            newTodo.user = request.user
            newTodo.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request,'todoapp/addtodo.html',{'form':TodoForm(),'error':'Введены некоректные данные, попробуйте снова'})
@login_required
def detailtodo(request,todo_id):
    todo = get_object_or_404(Todo,pk = todo_id, user = request.user)
    if request.method == 'GET':
        form = TodoForm(instance = todo)
        return render(request, 'todoapp/detailtodo.html', {'datatodo':todo,'form':form})
    else:
        try:
            infoForm = TodoForm(request.POST, instance = todo)
            infoForm.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request,'todoapp/detailtodo.html',{'form':TodoForm(instance = todo),'error':'Введены некоректные данные, попробуйте снова'})


@login_required
def compleatetodo(request,todo_id):
    todo = get_object_or_404(Todo,pk = todo_id, user = request.user)
    if request.method == 'POST':
        todo.datecompleat = timezone.now()
        todo.save()
        return redirect('currenttodos')
@login_required
def deletetodo(request,todo_id):
    todo = get_object_or_404(Todo,pk = todo_id, user = request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('currenttodos')
