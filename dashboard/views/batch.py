from django.shortcuts import redirect, render , get_object_or_404
from dashboard.models import *
from django.contrib import  messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from dashboard.models import CustomUser
from dashboard.forms.batch import BatchForm
from django.db.models import Q



def manager(request):
    return render(request, "dashboard/webpages/batch/manager.html")


def list(request):
    draw = int(request.GET.get("draw", 1))
    start = int(request.GET.get("start", 0))
    length = int(request.GET.get("length", 10))  
    search_value = request.GET.get("search[value]", "").strip()
    order_column = int(request.GET.get("order[0][column]", 0))
    order_dir = request.GET.get("order[0][dir]", "desc")
    
    batches = Batch.objects.filter(is_deleted=False)
    
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



def add(request):
    if request.method == "POST":
        form = BatchForm(request.POST, request.FILES)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.save()

            messages.success(request, "Customer added successfully!")
            return redirect('dashboard-batch')
        else:
            context = {
                "title": "Add Customer | Dashboard",
                "form": form,
            }
            return render(request, "dashboard/webpages/batch/add.html", context)
    else:
        form = BatchForm()  
        context = {
            "title": "Add Customer",
            "form": form,
        }
        return render(request, "dashboard/webpages/batch/add.html", context)


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