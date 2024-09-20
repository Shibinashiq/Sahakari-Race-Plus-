from dashboard.views.imports import *

@login_required(login_url='dashboard-login')
def manager(request):
    sort_option = request.GET.get('sort')
    
    start_date = request.GET.get('start_date', None)
    end_date = request.GET.get('end_date', None)

    if start_date and start_date.lower() != 'null':
        start_date = datetime.strptime(start_date, "%Y-%m-%d").strftime("%Y-%m-%d")
    else:
        start_date = None

    if end_date and end_date.lower() != 'null':
        end_date = (datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d")
    else:
        end_date = None
    
    user_filter = CustomUser.objects.filter(is_deleted=False, is_superuser=False, is_staff=True)
    
    if start_date and end_date:
        user_filter = user_filter.filter(created__range=[start_date, end_date])
    
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

    staff_count = user_filter.count()

    context = {
        "users": users,
        "current_sort": sort_option,
        "start_date": start_date,
        "end_date": end_date,
        "staff_count": staff_count,
    }

    return render(request, "ci/template/public/staff/staffs.html", context)


def list(request):
    print("hiiiiiiiiiiiiiiiiiiiiiiiiiiii")
    draw = int(request.GET.get("draw", 1))
    start = int(request.GET.get("start", 0))
    length = int(request.GET.get("length", 10))
    search_value = request.GET.get("search[value]", "").strip()
    order_column = int(request.GET.get("order[0][column]", 0))
    order_dir = request.GET.get("order[0][dir]", "desc")

    users = CustomUser.objects.filter(is_deleted=False,is_staff=True)
    print(users)

    order_columns = {
        0: 'id',
        1: 'name',
        4: 'phone_number',
    }

    order_field = order_columns.get(order_column, 'id')
    if order_dir == 'desc':
        order_field = '-' + order_field

    if search_value:
        users = users.filter(
            Q(name__icontains=search_value) |
            Q(phone_number__icontains=search_value) 
        )

    total_records = users.count()

    

    # users = users.order_by(order_field)

    paginator = Paginator(users, length)
    page_number = (start // length) + 1
    page_obj = paginator.get_page(page_number)

    data = []
    for user in page_obj:
       

        

        data.append({
            "id": user.id,
            "username": user.name if user.name else "N/A",
            "phone_number": user.phone_number if user.phone_number else "N/A",
            "created": timezone.localtime(user.created).strftime('%Y-%m-%d %H:%M:%S'),
            "is_disabled": user.is_active 
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
        form = StaffForm(request.POST, request.FILES)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.is_staff = True 
            customer.is_active = True               
            customer.save()
           

            

            messages.success(request, "Staff added successfully!")
            return redirect('dashboard-staff-manager')
        else:
            context = {
                "title": "Add staff | Dashboard",
                "form": form,
            }
            return render(request, "ci/template/public/staff/add-staff.html", context)
    else:
        form = StaffForm()  
        context = {
            "title": "Add Customer",
            "form": form,
        }
        return render(request, "ci/template/public/staff/add-staff.html", context)




@login_required(login_url='dashboard-login')
def update(request, pk):
    customer = get_object_or_404(CustomUser, pk=pk)
    if request.method == "POST":
        form = StaffForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            updated_customer = form.save(commit=False)
            updated_customer.is_staff = True  
            updated_customer.save()
            messages.success(request, "Customer updated successfully!")
            return redirect('dashboard-staff-manager')
        else:
            context = {
                "title": "Update Customer | Dashboard",
                "form": form,
            }
            return render(request, "ci/template/public/staff/update-staff.html", context)
    else:
        form = StaffForm(instance=customer)
        context = {
            "title": "Update Customer",
            "form": form,
        }
        return render(request, "ci/template/public/staff/update-staff.html", context)
    


@login_required(login_url='dashboard-login')
def disable(request,pk):
    if request.method == "GET":
        customer = get_object_or_404(CustomUser, pk=pk)
        if customer.is_active == False:
            customer.is_active = True
            messages.success(request, "Staff activated successfully!")
        else:
            customer.is_active = False
            messages.success(request, "Staff disabled successfully!")
        customer.save()
      
        return redirect('dashboard-staff-manager')
    else:
        messages.error(request, "Invalid request .")
        return redirect('dashboard-staff-manager')



@login_required(login_url='dashboard-login')
def set_password(request, pk):
    user = CustomUser.objects.get(pk=pk)

    if request.method == 'POST':
        form = PasswordSettingForm(request.POST, user_id=pk)
        if form.is_valid():
            form.save(user)
            messages.success(request, 'Password successfully updated!')
            return redirect('dashboard-staff-manager')
    else:
        form = PasswordSettingForm(user_id=pk)

    return render(request, 'dashboard/webpages/staff/password.html', {'form': form, 'pk': pk})



