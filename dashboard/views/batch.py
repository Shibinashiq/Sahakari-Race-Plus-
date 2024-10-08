from dashboard.views.imports import *

@login_required(login_url='dashboard-login')
def manager(request):
    sort_option = request.GET.get('sort')
    
    start_date = request.GET.get('start_date', None)
    end_date = request.GET.get('end_date', None)

    if start_date and start_date.lower() != 'null':
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    else:
        start_date = None

    if end_date and end_date.lower() != 'null':
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date() + timedelta(days=1)
    else:
        end_date = None

    batch_filter = Batch.objects.filter(is_deleted=False, batch_expiry__gte=timezone.now().date())
    
    if start_date and end_date:
        batch_filter = batch_filter.filter(start_date__range=[start_date, end_date])
    
    if sort_option == 'ascending':
        batches = batch_filter.order_by('id')
    elif sort_option == 'descending':
        batches = batch_filter.order_by('-id')
    elif sort_option == 'price_ascending':
        batches = batch_filter.order_by('batch_price')
    elif sort_option == 'price_descending':
        batches = batch_filter.order_by('-batch_price')
    else:
        batches = batch_filter.order_by('-id')
    paginator = Paginator(batches, 25)  
    page_number = request.GET.get('page')
    batches_paginated = paginator.get_page(page_number)

    context = {
        "batches": batches_paginated,
        "current_sort": sort_option,
        "start_date": start_date,
        "end_date": end_date,
    }

    return render(request, "ci/template/public/batch/batch.html", context)



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
            batch = form.save(commit=False)
            start_date = batch.start_date
            course = batch.course 

            current_date = timezone.now().date()
            available_days = (batch.batch_expiry - start_date).days + 1

            print(f"Available days: {available_days}")
            print(f"Course duration: {course.duration}")
            
            course_duration = int(course.duration)
            number_of_lessons = int(course.number_of_lessons)

            if course_duration > available_days: 
                batch.late_batch = True

            batch.save()

            if course_duration > available_days: 
                batch_id = batch.id  
                messages.warning(request, "Please specify merging days for the late batch.")
                return redirect(f"{reverse('dashboard-batch')}?showMergeDaysModal=true&batch={batch_id}")
            else:
                total_lessons = number_of_lessons
                course_duration_days = course_duration  
                lessons_per_day = total_lessons / course_duration_days

                lessons = Lesson.objects.filter(is_deleted=False, chapter__subject__course=course).order_by('created')

                visible_day_count = 1
                lesson_index = 0

                for day in range(course_duration_days):
                    for _ in range(int(lessons_per_day)):
                        if lesson_index >= len(lessons):
                            break

                        lesson = lessons[lesson_index]

                        BatchLesson.objects.create(
                            batch=batch,
                            lesson=lesson,
                            visible_in_days=str(visible_day_count),
                        )

                        lesson_index += 1

                    visible_day_count += 1

            messages.success(request, "Batch added successfully!")
            return redirect('dashboard-batch')
        else:
            messages.error(request, "Please correct the errors")

    else:
        form = BatchForm()
    
    context = {
        "title": "Add Batch",
        "form": form,
    }
    return render(request, "ci/template/public/batch/add-batch.html", context)





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
            return render(request, "ci/template/public/batch/update-batch.html", context)
    else:
        form = BatchForm(instance=batch)
        context = {
            "title": "Update Batch",
            "form": form,
            "batch": batch,
        }
        return render(request, "ci/template/public/batch/update-batch.html", context)




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
        messages.success(request, " deleted successfully!")
        return redirect('dashboard-batch-subscripton-manager',pk=batch_id)
    else:
        messages.error(request, "Invalid request .")
        return redirect('dashboard-batch-subscripton-manager',pk=batch_id)
    

def merge(request):
    merge_days = request.GET.get('merge_days')
    batch_id = request.GET.get('batch_id')
    print(merge_days,"merge_days")
    print(batch_id,"batch_id")
    if not merge_days or int(merge_days) <= 0:
        return HttpResponse("Invalid merge days provided.")

    batch = get_object_or_404(Batch, id=batch_id)
    course = batch.course

    total_lessons = int(course.number_of_lessons) 
    course_duration_days = int(course.duration)  

    lessons_per_day = total_lessons / course_duration_days

    batch_start_date = batch.start_date
    batch_end_date = batch.batch_expiry

    total_batch_days = (batch_end_date - batch_start_date)
    total_batch_days_count = total_batch_days.days

    late_days = course_duration_days - total_batch_days_count

    missed_lessons = int(late_days * lessons_per_day)

    total_merge_lessons = missed_lessons + int(merge_days) * lessons_per_day

    lessons_per_day_during_merge = int(total_merge_lessons) // int(merge_days)

    lessons = Lesson.objects.filter(is_deleted=False,chapter__subject__course=course).order_by('created')

    lessons_to_distribute = lessons[:int(total_merge_lessons)]

    visible_day_count = 1
    lesson_index = 0

    for day in range(int(merge_days)):
        for _ in range(lessons_per_day_during_merge):
            if lesson_index >= len(lessons_to_distribute):
                break

            lesson = lessons_to_distribute[lesson_index]

            BatchLesson.objects.create(
                batch=batch,
                lesson=lesson,
                visible_in_days=str(visible_day_count),
            )

            lesson_index += 1

        visible_day_count += 1

    remaining_lessons = lessons[lesson_index:]  
    remaining_days = course_duration_days - int(merge_days)  

    for lesson in remaining_lessons:
        BatchLesson.objects.create(
            batch=batch,
            lesson=lesson,
            visible_in_days=str(visible_day_count),  
        )
        visible_day_count += 1  

    return JsonResponse({'success': True, 'message': 'Lessons successfully merged and scheduled.'})



@login_required(login_url='dashboard-login')
def schedule(request, pk):
    batch = get_object_or_404(Batch, id=pk)
    course = batch.course

    chapters = Chapter.objects.filter(subject__course=course, is_deleted=False)
    folders = Folder.objects.filter(chapter__in=chapters, is_deleted=False)
    lessons_from_folders = Lesson.objects.filter(folder__in=folders, is_deleted=False)
    lessons_from_chapters = Lesson.objects.filter(chapter__in=chapters, is_deleted=False)

    lessons = lessons_from_folders | lessons_from_chapters

    batch_lessons = BatchLesson.objects.filter(is_deleted=False, batch=batch).order_by('visible_in_days')
   

    context = {
        'batch': batch,
        'batch_lessons': batch_lessons, 
    }

    return render(request, 'ci/template/public/batch/schedule.html', context)







