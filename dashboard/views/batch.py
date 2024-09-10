from dashboard.views.imports import *

@login_required(login_url='dashboard-login')
def manager(request):
    return render(request, "dashboard/webpages/batch/manager.html")




@login_required(login_url='dashboard-login')
def list(request):
    draw = int(request.GET.get("draw", 1))
    start = int(request.GET.get("start", 0))
    length = int(request.GET.get("length", 10))  
    search_value = request.GET.get("search[value]", "").strip()
    order_column = int(request.GET.get("order[0][column]", 0))
    order_dir = request.GET.get("order[0][dir]", "desc")
    

    batches = Batch.objects.filter(is_deleted=False, batch_expiry__gte=timezone.now().date())

    
    order_columns = {
        0: 'id',
        1: 'course__course_name',  
        2: 'batch_price', 
        3: 'created',
        4: 'batch_expiry',

    }
    
    order_field = order_columns.get(order_column, 'id')
    if order_dir == 'desc':
        order_field = '-' + order_field
    
    if search_value:
        batches = batches.filter(
            Q(course__course_name__icontains=search_value) |
            Q(batch_price__icontains=search_value) |
            Q(created__icontains=search_value) |
            Q(batch_expiry__icontains=search_value)
        )
    
    total_records = batches.count()

    batches = batches.order_by(order_field)

    paginator = Paginator(batches, length)
    page_number = (start // length) + 1
    page_obj = paginator.get_page(page_number)

    data = []
    for batch in page_obj:
        data.append({
            "id": batch.id,
            "course": batch.course.course_name if batch.course.course_name else "N/A",
            "price": str(batch.batch_price) if batch.batch_price else "N/A",
            "start_date": batch.start_date.strftime("%Y-%m-%d") if batch.start_date else "N/A",
            "end_date": batch.batch_expiry.strftime("%Y-%m-%d") if batch.batch_expiry else "N/A",
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
        form = BatchForm(request.POST, request.FILES)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.save()

            messages.success(request, "Batch added successfully!")
            return redirect('dashboard-batch')
        else:
            context = {
                "title": "Add Batch | Dashboard",
                "form": form,
            }
            return render(request, "dashboard/webpages/batch/add.html", context)
    else:
        form = BatchForm()  
        context = {
            "title": "Add Batch",
            "form": form,
        }
        return render(request, "dashboard/webpages/batch/add.html", context)




@login_required(login_url='dashboard-login')
def update(request, pk):
    batch = get_object_or_404(Batch, pk=pk, is_deleted=False)
    
    if request.method == "POST":
        form = BatchForm(request.POST, request.FILES, instance=batch)
        if form.is_valid():
            form.save()
            messages.success(request, "Batch updated successfully!")
            return redirect('dashboard-batch')
        else:
            context = {
                "title": "Update Batch | Dashboard",
                "form": form,
                "batch": batch,
            }
            return render(request, "dashboard/webpages/batch/update.html", context)
    else:
        form = BatchForm(instance=batch)
        context = {
            "title": "Update Batch",
            "form": form,
            "batch": batch,
        }
        return render(request, "dashboard/webpages/batch/update.html", context)




@login_required(login_url='dashboard-login')
def delete(request, pk):
    if request.method == "POST":
        batch = get_object_or_404(Batch, pk=pk)
        batch.is_deleted = True
        batch.save()
        messages.success(request, "Batch deleted successfully!")
        return redirect('dashboard-batch')
    else:
        messages.error(request, "Invalid request .")
        return redirect('dashboard-batch')
    

@login_required(login_url='dashboard-login')
def subscription_view(request,pk):
    context={
        "pk": pk 
    }
    return render(request, "dashboard/webpages/batch/customer.html",context)


@login_required(login_url='dashboard-login')
def subscription(request, pk): 
    draw = int(request.GET.get("draw", 1))
    start = int(request.GET.get("start", 0))
    length = int(request.GET.get("length", 10))
    search_value = request.GET.get("search[value]", "").strip()
    order_column = int(request.GET.get("order[0][column]", 0))
    order_dir = request.GET.get("order[0][dir]", "desc")

    subscriptions = Subscription.objects.filter(batch__id=pk, is_deleted=False)

    users = CustomUser.objects.filter(
        subscription__in=subscriptions,  
        is_deleted=False
    )

    order_columns = {
        0: 'id',
        1: 'name',
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
        Prefetch(
            'subscription_set',
            queryset=Subscription.objects.filter(is_deleted=False).prefetch_related('batch__course')
        )
    )

    paginator = Paginator(users, length)
    page_number = (start // length) + 1
    page_obj = paginator.get_page(page_number)

    data = []
    for user in page_obj:
        user_subscriptions = user.subscription_set.filter(batch__id=pk)

        subscription_details = []
        for subscription in user_subscriptions:
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
def add_customer(request, batch_id):
    if request.method == "POST":
        form = BatchCustomerForm(request.POST, request.FILES)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.save()

            batch = Batch.objects.get(id=batch_id)
            subscription = Subscription.objects.create(user=customer)
          
            subscription.batch.add(batch) 
            subscription.save()

            messages.success(request, "Customer added successfully!")
            return redirect('dashboard-batch-subscripton-manager', pk=batch_id)
        else:
            context = {
                "title": "Add Customer | Dashboard",
                "form": form,
                "batch_id":batch_id
            }
            return render(request, "dashboard/webpages/batch/customer_add .html", context)
    else:
        form = BatchCustomerForm()  
        context = {
            "title": "Add Customer",
            "form": form,
             "batch_id":batch_id
        }
        return render(request, "dashboard/webpages/batch/customer_add .html", context)




@login_required(login_url='dashboard-login')
def update_customer(request, batch_id,customer_id):
    customer = get_object_or_404(CustomUser, pk=customer_id)
    if request.method == "POST":
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            updated_customer = form.save(commit=False)
            updated_customer.save()

            batches = form.cleaned_data.get('batches',None)
            subscription = Subscription.objects.get(user=updated_customer)
            subscription.batch .set(batches)  
            subscription.save()

            messages.success(request, "Customer updated successfully!")
            return redirect('dashboard-batch-subscripton-manager',pk=batch_id)
        else:
            context = {
                "title": "Update Customer | Dashboard",
                "form": form,
            }
            return render(request, "dashboard/webpages/batch/customer_update.html", context)
    else:
        form = CustomerForm(instance=customer)
        context = {
            "title": "Update Customer",
            "form": form,
        }
        return render(request, "dashboard/webpages/batch/customer_update.html", context)
    


@login_required(login_url='dashboard-login')
def delete_customer(request, customer_id,batch_id):
    if request.method == "POST":
        customer = get_object_or_404(CustomUser, pk=customer_id)
        customer.is_deleted = True
        customer.save()
        messages.success(request, "Customer deleted successfully!")
        return redirect('dashboard-batch-subscripton-manager',pk=batch_id)
    else:
        messages.error(request, "Invalid request .")
        return redirect('dashboard-batch-subscripton-manager',pk=batch_id)
    
