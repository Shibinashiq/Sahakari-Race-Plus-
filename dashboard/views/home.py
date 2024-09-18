from dashboard.views.imports import *

@login_required(login_url='dashboard-login')
def home(request):
    user=request.user
    customers = CustomUser.objects.filter(is_deleted=False,is_staff=False,is_superuser=False).count()
    staff = CustomUser.objects.filter(is_deleted=False,is_staff=True,is_superuser=False).count()
    course=Course.objects.filter(is_deleted=False).count()
    subscription = Subscription.objects.filter(is_deleted=False).count()

    context = {
        "title": "Home | Agua Dashboard",
        "user": user,
        "customers": customers,
        "staff": staff,
        "course": course,
        "subscription": subscription,

    }

    return render(request, "ci/template/public/index.html",context)