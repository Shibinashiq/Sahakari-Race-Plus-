from dashboard.views.imports import *

@login_required(login_url='dashboard-login')
def home(request):
    user = request.user
    created = CustomUser.objects.filter(id=user.id)
    print(created)
    
    customers = CustomUser.objects.filter(is_deleted=False, is_staff=False, is_superuser=False).count()
    
    staff = CustomUser.objects.filter(is_deleted=False, is_staff=True, is_superuser=False).count()
    in_active_staff = CustomUser.objects.filter(is_deleted=False, is_staff=True, is_superuser=False, is_active=False).count()
    active_staff = CustomUser.objects.filter(is_deleted=False, is_staff=True, is_superuser=False, is_active=True).count()
    
    course = Course.objects.filter(is_deleted=False).count()
    
    subscription = Subscription.objects.filter(is_deleted=False).count()

    subscribed_users = CustomUser.objects.filter(subscription__is_deleted=False,is_deleted=False).distinct().count()

    non_subscribed_users = CustomUser.objects.filter(is_deleted=False, is_staff=False, is_superuser=False).exclude(subscription__is_deleted=False).distinct().count()
    course_with_most_subscriptions = (
        Course.objects.filter(is_deleted=False,batch__subscription__is_deleted=False)
        .annotate(sub_count=Count('batch__subscription', distinct=True))  
        .order_by('-sub_count')
        .first()
    )

    most_subscribed_course_name = course_with_most_subscriptions.course_name if course_with_most_subscriptions else None
    most_subscribed_course_count = course_with_most_subscriptions.sub_count if course_with_most_subscriptions else 0


    # print(most_subscribed_course_count)
    # print(most_subscribed_course_name)
    context = {
        "user": user,
        "customers": customers,

        "staff": staff,
        "in_active_staff":in_active_staff,
        "active_staff":active_staff,


        "course": course,
        "most_subscribed_course_count":most_subscribed_course_count,

        "subscription": subscription,
        "subscribed_users": subscribed_users,
        "non_subscribed_users": non_subscribed_users,
        "most_subscribed_course_name":most_subscribed_course_name

    }

    return render(request, "ci/template/public/home/index.html", context)