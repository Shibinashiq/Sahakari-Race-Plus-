from django.shortcuts import redirect, render
from dashboard.models import *
from django.contrib.auth.decorators import login_required


@login_required(login_url='dashboard-login')
def home(request):
    user=request.user
    print(user)
    customers = CustomUser.objects.filter(is_deleted=False).exclude(id=user.id).count()
    course=Course.objects.filter(is_deleted=False).count()
    subscription = Subscription.objects.filter(is_deleted=False).count()

    context = {
        "title": "Home | Agua Dashboard",
        "user": user,
        "customers": customers,
        "course": course,
        "subscription": subscription,

    }

    return render(request, "dashboard/home/index.html",context)