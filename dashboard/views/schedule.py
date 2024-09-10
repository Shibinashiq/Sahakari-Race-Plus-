from django.shortcuts import redirect, render , get_object_or_404
from dashboard.models import *
from django.contrib import  messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from dashboard.models import CustomUser
from dashboard.forms.schedule import ScheduleForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required


@login_required(login_url='dashboard-login')
def manager(request):
    return render(request, 'dashboard/webpages/schedule/manager.html')



@login_required(login_url='dashboard-login')
def list(request):
    draw = int(request.GET.get("draw", 1))
    start = int(request.GET.get("start", 0))
    length = int(request.GET.get("length", 10))
    search_value = request.GET.get("search[value]", "")
    order_column = int(request.GET.get("order[0][column]", 0))
    order_dir = request.GET.get("order[0][dir]", "desc")
    
    order_columns = {
        0: 'id',
        1: 'title',
        2: 'lesson',
        3: 'exam',
        4: 'date'
    }
    
    order_field = order_columns.get(order_column, 'id')
    if order_dir == 'desc':
        order_field = '-' + order_field
    
    schedule = Schedule.objects.filter(is_deleted=False)
    
    if search_value:
        schedule = schedule.filter(
            Q(title__icontains=search_value) |
            Q(lesson__lesson_name__icontains=search_value) |
            Q(exam__title__icontains=search_value)
        )
    
    total_records = schedule.count()

    schedule = schedule.order_by(order_field)
    paginator = Paginator(schedule, length)
    page_number = (start // length) + 1
    page_obj = paginator.get_page(page_number)

    data = []
    for schedule in page_obj:
       
        
        data.append({
            "id": schedule.id,
            "title": schedule.title if schedule.title else "N/A",
            "lesson": schedule.lesson.lesson_name if schedule.lesson else "N/A",
            "exam": schedule.exam.title if schedule.exam else "N/A",
            "date":timezone.localtime(schedule.date).strftime('%Y-%m-%d %H:%M:%S')
             
            
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
    if request.method == 'POST':
        form = ScheduleForm(request.POST)  
        if form.is_valid():

            form.save()
            messages.success(request, "Schedule added successfully.")
            return redirect('dashboard-schedule-manager')  
        else:
            return render(request, 'dashboard/webpages/schedule/add.html', {'form': form})

    else:
        form = ScheduleForm()  

    return render(request, 'dashboard/webpages/schedule/add.html', {'form': form})



@login_required(login_url='dashboard-login')
def update(request, pk):
    schedule = get_object_or_404(Schedule, pk=pk)
    
    if request.method == 'POST':
        form = ScheduleForm(request.POST, instance=schedule)  
        
        if form.is_valid():
            form.save()  
            messages.success(request, "Schedule updated successfully.")
            return redirect('dashboard-schedule-manager')  
        else:
            return render(request, 'dashboard/webpages/schedule/update.html', {'form': form})

    else:
        form = ScheduleForm(instance=schedule)  

    return render(request, 'dashboard/webpages/schedule/update.html', {'form': form})


@login_required(login_url='dashboard-login')
def delete(request, pk):
    if request.method == 'POST':
        schedule = get_object_or_404(Schedule, pk=pk)
        schedule.is_deleted = True
        schedule.save()
        messages.success(request, 'Schedule deleted successfully.')
        return redirect('dashboard-schedule-manager')
    messages.error(request, 'Failed to delete Schedule.')
    return redirect('dashboard-schedule-manager')
   