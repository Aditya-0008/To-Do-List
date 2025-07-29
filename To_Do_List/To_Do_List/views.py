from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from To_Do_List import models
from To_Do_List.models import TODOO
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def signup(request):
    if request.method == 'POST':
        fnm = request.POST.get('fnm')
        email = request.POST.get('email')
        pwd = request.POST.get('pwd')

        # Check if username or email already exists
        if User.objects.filter(username=fnm).exists():
            return render(request, 'signup.html', {'error': 'Username already exists'})
        elif User.objects.filter(email=email).exists():
            return render(request, 'signup.html', {'error': 'Email already exists'})
        
        # If not exists, create new user
        my_user = User.objects.create_user(fnm, email, pwd)
        my_user.save()
        return redirect('/loginn')

    return render(request, 'signup.html')

def loginn(request):
    if request.method == 'POST':
        fnm = request.POST.get('fnm')
        email = request.POST.get('email')
        pwd = request.POST.get('pwd')

        user_qs = User.objects.filter(username=fnm, email=email)
        if not user_qs.exists():
            return render(request, 'login.html', {'error': 'Account does not exist'})

        userr = authenticate(request, username=fnm, password=pwd)
        if userr is not None:
            login(request, userr)
            return redirect('/todopage')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')

@login_required(login_url='/loginn')
def todo(request):
    if request.method=='POST':
        title=request.POST.get('title')
        print(title)
        obj=models.TODOO(title=title, user=request.user)
        obj.save()
        user=request.user
        res=models.TODOO.objects.filter(user=user).order_by('-date')
        return redirect('/todopage', {'res': res})
    
    res=models.TODOO.objects.filter(user=request.user).order_by('-date')
    return render(request, 'todo.html', {'res': res})

@login_required(login_url='/loginn')
def edit_todo(request, srno):
    obj = models.TODOO.objects.get(srno=srno)
    if request.method == 'POST':
        title = request.POST.get('title')
        obj.title = title
        obj.save()
        return redirect('/todopage')
    
    res = models.TODOO.objects.filter(user=request.user).order_by('-date')
    return render(request, 'edit_todo.html', {'obj': obj, 'res': res})

@login_required(login_url='/loginn')
def delete_todo(request, srno):
    obj=models.TODOO.objects.get(srno=srno)
    obj.delete()
    return redirect('/todopage')

def signout(request):
    logout(request)
    return redirect('/loginn')

def toggle_complete(request, srno):
    todo = TODOO.objects.get(srno=srno)
    todo.completed = not todo.completed
    todo.save()
    return redirect('/todopage')