

from dashboard.views.imports import *

def login(request):
    if 'username' in request.session:
        return redirect('/')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password) 
        
        if user is not None:
            auth_login(request, user) 
            request.session['username'] = username
            messages.success(request, 'Admin Logged in!')
            return redirect('/')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('login/')
    else:
        return render(request, "ci/template/public/login/login.html")


# def home(request):
#     return render(request, "ci/template/public/index.html")  