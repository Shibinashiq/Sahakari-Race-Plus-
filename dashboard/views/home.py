from django.shortcuts import redirect, render


def home(request):
    user=request.user
    context = {
        "title": "Home | Agua Dashboard",
        "user": user,
    }

    return render(request, "dashboard/home/index.html",context)