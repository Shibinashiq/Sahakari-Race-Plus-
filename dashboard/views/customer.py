from dashboard.views.imports import *

@login_required(login_url='dashboard-login')
def manager(request):
    sort_option = request.GET.get('sort')
    
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if end_date:
        end_date = (datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d")
    if start_date:
        start_date = (datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d")
    user_filter = CustomUser.objects.filter(is_deleted=False, is_staff=False, is_superuser=False)
    
    if start_date and end_date:
        user_filter = user_filter.filter(created__range=[start_date, end_date])
    else:
        start_date = None
        end_date = None
    
    if sort_option == 'ascending':
        user_list = user_filter.order_by('id')
    elif sort_option == 'descending':
        user_list = user_filter.order_by('-id')
    elif sort_option == 'name_ascending':
        user_list = user_filter.order_by('name')
    elif sort_option == 'name_descending':
        user_list = user_filter.order_by('-name')
    else:
        user_list = user_filter.order_by('-id')

    paginator = Paginator(user_list, 25)
    page_number = request.GET.get('page')
    users = paginator.get_page(page_number)

    context = {
        "users": users,
        "current_sort": sort_option,
        "start_date": start_date,
        "end_date": end_date
    }

    return render(request, "ci/template/public/student/student_grid.html", context)









@login_required(login_url='dashboard-login')
def list(request):
    draw = int(request.GET.get("draw", 1))
    start = int(request.GET.get("start", 0))
    length = int(request.GET.get("length", 10))
    search_value = request.GET.get("search[value]", "").strip()
    order_column = int(request.GET.get("order[0][column]", 0))
    order_dir = request.GET.get("order[0][dir]", "desc")

    users = CustomUser.objects.filter(is_deleted=False,is_staff=False,is_superuser=False)

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

    active_batches_prefetch = Prefetch(
      'subscription_set', 
     queryset=Subscription.objects.filter(
        is_deleted=False
     ).prefetch_related(
        Prefetch(
            'batch',
            queryset=Batch.objects.filter(
                batch_expiry__gte=timezone.now().date(),
                is_deleted=False
            ).select_related('course')
        )
    )
    ) 

    users = users.order_by(order_field).prefetch_related(active_batches_prefetch)

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
            messages.success(request, "Customer added successfully!")
            return redirect('dashboard-customer')
        else:
            context = {
                "title": "Add Customer | Dashboard",
                "form": form,
            }
            return render(request, "ci/template/public/student/add-student.html", context)
    else:
        form = CustomerForm()  
        context = {
            "title": "Add Customer",
            "form": form,
        }
        return render(request, "ci/template/public/student/add-student.html", context)



@login_required(login_url='dashboard-login')
def update(request, pk):
    customer = get_object_or_404(CustomUser, pk=pk)
    if request.method == "POST":
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            updated_customer = form.save(commit=False)
            updated_customer.save()

            batches = form.cleaned_data.get('batches')

            subscriptions = Subscription.objects.filter(user=updated_customer, is_deleted=False)

            if subscriptions.exists():
                subscription = subscriptions.first()
                subscription.batch.set(batches)
                
                subscriptions.exclude(id=subscription.id).delete()

            else:
                subscription = Subscription.objects.create(user=updated_customer)
                subscription.batch.add(*batches)

            subscription.save()

            messages.success(request, "Customer updated successfully!")
            return redirect('dashboard-customer')
        else:
            context = {
                "title": "Update Customer | Dashboard",
                "form": form,
            }
            return render(request, "ci/template/public/student/update-student.html", context)
    else:
        form = CustomerForm(instance=customer)
        context = {
            "title": "Update Customer",
            "form": form,
        }
        return render(request, "ci/template/public/student/update-student.html", context)



@login_required(login_url='dashboard-login')
def delete(request,pk):
    print("Delete request received 1")
    if request.method == "POST":
        print("Delete request received")
        customer = get_object_or_404(CustomUser, pk=pk)
        customer.is_deleted = True
        customer.save()
        messages.success(request, "Customer deleted successfully!")
        return redirect('dashboard-customer')
    else:
        messages.error(request, "Invalid request .")
        return redirect('dashboard-customer')
    

from django.db.models import Count
    
def detail(request, pk):
    customer = get_object_or_404(CustomUser, pk=pk)
    subscriptions = Subscription.objects.filter(user=customer, is_deleted=False).prefetch_related('batch')
    
    batches = Batch.objects.filter(subscription__in=subscriptions).distinct()

    courses = Course.objects.filter(batch__in=batches).distinct()

    unique_batches_count = subscriptions.aggregate(
        total_batches=Count('batch', distinct=True)
    )['total_batches']

    context = {
        "title": "Customer Detail",
        "customer": customer,
        "subscriptions": subscriptions,
        "sub_count": unique_batches_count,
        "courses": courses  
    }
    
    return render(request, "ci/template/public/student/student-details.html", context)
    






@login_required(login_url='dashboard-login')
def subscription_customer_update(request,pk):
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
            return redirect('dashboard-user-detail',pk)
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
def subscription_add(request, pk):
    customer = CustomUser.objects.get(id=pk, is_deleted=False)

    if request.method == "POST":
        form = SubscriptionCustomerForm(request.POST, request.FILES, customer=customer)
        if form.is_valid():
            batch = form.cleaned_data.get('batch')

            # Create or get existing subscription
            subscription, created = Subscription.objects.get_or_create(user=customer,is_deleted=False)
            
            if batch:
                if subscription.batch.filter(id=batch.id).exists():
                    messages.error(request, "This batch is already added to the subscription.")
                else:
                    subscription.batch.add(batch)
                    messages.success(request, "Subscription added successfully!")
            
            subscription.save()
            return redirect('dashboard-user-detail', pk)
        else:
            context = {
                "form": form,
                "pk": pk
            }
            return render(request, "dashboard/webpages/customer/batch_add.html", context)
    else:
        form = SubscriptionCustomerForm(customer=customer)
        context = {
            "title": "Add Batch",
            "form": form,
            "pk": pk
        }
        return render(request, "dashboard/webpages/customer/batch_add.html", context)




@login_required(login_url='dashboard-login')
def subscription_delete(request,pk):
    if request.method == 'POST':
        subscription= Subscription.objects.get(id=pk)
        user_id=subscription.user.id
        subscription.is_deleted = True
        subscription.save()
        messages.success(request, " deleted successfully!")
        return redirect('dashboard-user-detail',pk=user_id)
    else:
        messages.success(request, " Action denied!")
        return redirect('dashboard-user-detail',pk=user_id)




def result(request,pk):
    return render(request,'ci/template/public/student/student-result.html')