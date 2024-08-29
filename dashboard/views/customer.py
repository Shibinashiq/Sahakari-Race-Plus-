from django.shortcuts import redirect, render , get_object_or_404
from dashboard.models import *
from django.contrib import auth, messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from dashboard.models import CustomUser
from dashboard.forms.customer import CustomerForm
def manager(request):
    return render(request, "dashboard/webpages/customer/manager.html")



def customer_list(request):
    draw = int(request.GET.get("draw", 1))
    start = int(request.GET.get("start", 0))
    length = int(request.GET.get("length", 10))  
    search_value = request.GET.get("search[value]", "")
    order_column = int(request.GET.get("order[0][column]", 0))
    order_dir = request.GET.get("order[0][dir]", "desc")
    
    users = CustomUser.objects.filter(is_deleted=False)
    
    order_columns = {
        0: 'id',
        1: 'username',  
        2: 'email',  
        3: 'district', 
        4: 'phone_number',
    }
    
    order_field = order_columns.get(order_column, 'id')
    if order_dir == 'desc':
        order_field = '-' + order_field
    
    if search_value:
        users = users.filter(username__icontains=search_value)
    
    total_records = users.count()

    users = users.order_by(order_field)

    paginator = Paginator(users, length)
    page_number = (start // length) + 1
    page_obj = paginator.get_page(page_number)

    data = []
    for user in page_obj:
        data.append({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "district": user.get_district_display(), 
            "phone_number": user.phone_number,
            "created":user.created_at.strftime("%d-%m-%Y %H:%M:%S"),
        })
    
    response = {
        "draw": draw,
        "recordsTotal": total_records,
        "recordsFiltered": total_records,
        "data": data,
    }

    return JsonResponse(response)







def customer_add(request):
    if request.method == "POST":
            form = CustomerForm(request.POST, request.FILES)
            if form.is_valid():
                course = form.save(commit=False)

                course_fee = form.cleaned_data.get('course_fee')
                course_expire = form.cleaned_data.get('course_expire')

                course.save()

                Batch.objects.create(
                    course=course,
                    batch_price=course_fee,
                    batch_expiry=course_expire
                )

                messages.success(request, "Course and Batch information added successfully!")
                return redirect('dashboard-course')
            else:
                context = {
                    "title": "Add Course | Dashboard",
                    "form": form,
                }
                return render(request, "dashboard/webpages/course/manager.html", context)
    else:
            form = CustomerForm()  
            context = {
                "title": "Add Course | Agua Dashboard",
                "form": form,
            }
            return render(request, "dashboard/webpages/course/manager.html", context)
