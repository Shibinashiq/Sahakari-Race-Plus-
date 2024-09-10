from django.shortcuts import redirect, render , get_object_or_404
from dashboard.models import *
from django.contrib import  messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from dashboard.models import CustomUser
from dashboard.forms.customer import CustomerForm
from django.db.models import Q ,Prefetch
from django.contrib.auth.decorators import login_required


@login_required(login_url='dashboard-login')
def manager(request):
    return render(request, "dashboard/webpages/customer/manager.html")



@login_required(login_url='dashboard-login')
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

    users = users.order_by(order_field).prefetch_related(
        Prefetch('subscription_set', queryset=Subscription.objects.filter(is_deleted=False).prefetch_related('batch__course'))
    )

    paginator = Paginator(users, length)
    page_number = (start // length) + 1
    page_obj = paginator.get_page(page_number)

    data = []
    for user in page_obj:
        subscriptions = user.subscription_set.all()
        subscription_details = []

        for subscription in subscriptions:
            for batch in subscription.batch.all():
                course_name = getattr(batch.course, "course_name", "N/A")
                start_date = batch.start_date.strftime("%d-%m-%Y") if batch.start_date else "N/A"
                expiry_date = batch.batch_expiry.strftime("%d-%m-%Y") if batch.batch_expiry else "N/A"
                subscription_details.append(
                    f'<span style="color: blue;">{course_name}</span> '
                    f'(<span style="color: green;">Start: {start_date}, '
                    f'<span style="color: red;">Expiry: {expiry_date}</span>)'
                )

        subscriptions_display = '<br>'.join(subscription_details) if subscription_details else "N/A"

        data.append({
            "id": user.id,
            "username": user.name if user.name else "N/A",
            "email": user.email if user.email else "N/A",
            "district": user.get_district_display() if user.district else "N/A",
            "phone_number": user.phone_number if user.phone_number else "N/A",
            "batch_names_display": subscriptions_display,
           "created": timezone.localtime(user.created).strftime('%Y-%m-%d %H:%M:%S')
        })

    response = {
        "draw": draw,
        "recordsTotal": total_records,
        "recordsFiltered": total_records,
        "data": data,
    }

    return JsonResponse(response)




@login_required(login_url='dashboard-login')
def add(request):
    if request.method == "POST":
        form = CustomerForm(request.POST, request.FILES)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.save()
            # batches = form.cleaned_data.get('batches')
            # subscription = Subscription.objects.create(user=customer)  
            # subscription.batch.set(batches)  
            # subscription.save()

            

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




@login_required(login_url='dashboard-login')
def update(request, pk):
    customer = get_object_or_404(CustomUser, pk=pk)
    if request.method == "POST":
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            updated_customer = form.save(commit=False)
            updated_customer.save()

            batches = form.cleaned_data.get('batches')
            subscription = Subscription.objects.get(user=updated_customer)
            subscription.batch  .set(batches)  
            subscription.save()

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
    


@login_required(login_url='dashboard-login')
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
    


    
@login_required(login_url='dashboard-login')
def detail(request, pk):
    customer = get_object_or_404(CustomUser, pk=pk)
    context = {
        "title": "Customer Detail",
        "customer": customer,
    }
    return render (request,"dashboard/webpages/customer/detail.html",context)
    
    








