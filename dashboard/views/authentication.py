from datetime import datetime

from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render



def login(request):
   
    if 'username' in request.session:
        return redirect('/')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(request, username=username, password=password)
        request.session['username'] = username
        auth.login(request, user)
        messages.success(request, 'Admin Logged in!')
        return redirect('/')

       
    else:
        return render(request, "dashboard/webpages/authentication/login.html")



def home(request):
    return render(request, "dashboard/webpages/home/index.html")  