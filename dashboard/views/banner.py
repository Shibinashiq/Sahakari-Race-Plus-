from dashboard.views.imports import *

def manager(request):
    return render (request,'dashboard/webpages/banner/manager.html')    

def list(request):
    draw = int(request.GET.get("draw", 1))
    start = int(request.GET.get("start", 0))
    length = int(request.GET.get("length", 10))
    search_value = request.GET.get("search[value]", "").strip()
    order_column = int(request.GET.get("order[0][column]", 0))
    order_dir = request.GET.get("order[0][dir]", "desc")

    users = None
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


def add(request):
    pass


def update(request,pk):
    pass


def delete(request,pk):
    pass