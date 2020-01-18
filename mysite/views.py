from django.shortcuts import render, get_object_or_404, redirect,reverse
from django.contrib import auth

def home(request):
    context={}
    return render(request,'home.html',context)

def login(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    referer=request.META.get('HTTP_REFERER',reverse('home'))
    user = auth.authenticate(request, username=username, password=password)
    if user is not None:
        auth.login(request, user)
        return redirect(referer)
    else:
        return render(request, 'error.html', {'message':'用户名或密码不正确'})