from django.shortcuts import redirect, render , get_object_or_404
from dashboard.models import *
from django.contrib import  messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from dashboard.models import CustomUser
from dashboard.forms.customer import CustomerForm
from django.db.models import Q




def manager(request):
    return render(request, "dashboard/webpages/customer/manager.html")

def list(request):
    draw = int(request.GET.get("draw", 1))
    start = int(request.GET.get("start", 0))
    length = int(request.GET.get("length", 10))  
    search_value = request.GET.get("search[value]", "").strip()
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
        users = users.filter(
            Q(name__icontains=search_value) |
            Q(phone_number__icontains=search_value) |
            Q(district__icontains=search_value) |
            Q(email__icontains=search_value)
        )
    
    total_records = users.count()

    users = users.order_by(order_field)

    paginator = Paginator(users, length)
    page_number = (start // length) + 1
    page_obj = paginator.get_page(page_number)

    data = []
    for user in page_obj:
        subscriptions = Subscription.objects.filter(user=user)
        subscription_details = [
            f'<span style="color: blue;">{subscription.batch.course.course_name}</span> (<span style="color: green;">Start: {subscription.batch.start_date.strftime("%d-%m-%Y")}, <span style="color: red;">Expiry: {subscription.batch.batch_expiry.strftime("%d-%m-%Y")}</span>)'
            for subscription in subscriptions
        ]
        subscriptions_display = '<br>'.join(subscription_details) if subscription_details else "N/A"
        data.append({
            "id": user.id,
            "username": user.name if user.name else "N/A",
            "email": user.email if user.email else "N/A",
            "district": user.get_district_display() if user.district else "N/A", 
            "phone_number": user.phone_number if user.phone_number else "N/A",
            "batch_names_display":subscriptions_display,
            "created": user.created.strftime("%d-%m-%Y %H:%M:%S"),
        })
    
    response = {
        "draw": draw,
        "recordsTotal": total_records,
        "recordsFiltered": total_records,
        "data": data,
    }

    return JsonResponse(response)






def add(request):
    if request.method == "POST":
        form = CustomerForm(request.POST, request.FILES)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.save()
            batches = form.cleaned_data.get('batches')
            Subscription.objects.filter(user=customer).delete() 
            for batch in batches:
                Subscription.objects.create(user=customer, batch=batch)
           

            

            messages.success(request, "Customer added successfully!")
            return redirect('dashboard-customer')
        else:
            context = {
                "title": "Add Customer | Dashboard",
                "form": form,
            }
            return render(request, "dashboard/webpages/customer/add.html", context)
    else:
        form = CustomerForm()  
        context = {
            "title": "Add Customer",
            "form": form,
        }
        return render(request, "dashboard/webpages/customer/add.html", context)


def update(request, pk):
    customer = get_object_or_404(CustomUser, pk=pk)
    if request.method == "POST":
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            updated_customer = form.save(commit=False)
            batch = form.cleaned_data.get('batch')
            updated_customer.save()

            Subscription.objects.update_or_create(
                user=updated_customer,
                defaults={'batch': batch}
            )

            messages.success(request, "Customer updated successfully!")
            return redirect('dashboard-customer')
        else:
            context = {
                "title": "Update Customer | Dashboard",
                "form": form,
            }
            return render(request, "dashboard/webpages/customer/update.html", context)
    else:
        form = CustomerForm(instance=customer)
        context = {
            "title": "Update Customer",
            "form": form,
        }
        return render(request, "dashboard/webpages/customer/update.html", context)
    



def delete(request,pk):
    if request.method == "POST":
        customer = get_object_or_404(CustomUser, pk=pk)
        customer.is_deleted = True
        customer.save()
        messages.success(request, "Customer deleted successfully!")
        return redirect('dashboard-customer')
    else:
        messages.error(request, "Invalid request .")
        return redirect('dashboard-customer')
    

def detail(request, pk):
    customer = get_object_or_404(CustomUser, pk=pk)
    context = {
        "title": "Customer Detail",
        "customer": customer,
    }
    return render (request,"dashboard/webpages/customer/detail.html",context)
    
    








