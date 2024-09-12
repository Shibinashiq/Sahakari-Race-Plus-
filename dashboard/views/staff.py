from dashboard.views.imports import *

def manager(request):
    return render (request,'dashboard/webpages/staff/manager.html')



def list(request):
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
            customer.save()
           

            

            messages.success(request, "Staff added successfully!")
            return redirect('dashboard-staff-manager')
        else:
            context = {
                "title": "Add staff | Dashboard",
                "form": form,
            }
            return render(request, "dashboard/webpages/staff/add.html", context)
    else:
        form = StaffForm()  
        context = {
            "title": "Add Customer",
            "form": form,
        }
        return render(request, "dashboard/webpages/staff/add.html", context)




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
            return render(request, "dashboard/webpages/staff/update.html", context)
    else:
        form = StaffForm(instance=customer)
        context = {
            "title": "Update Customer",
            "form": form,
        }
        return render(request, "dashboard/webpages/staff/update.html", context)
    


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