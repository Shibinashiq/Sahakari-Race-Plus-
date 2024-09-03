from django.shortcuts import redirect, render , get_object_or_404
from dashboard.models import *
from django.contrib import  messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from dashboard.models import CustomUser
from dashboard.forms.exam import ExamForm
from django.db.models import Q

def manager(request):
    return render(request, "dashboard/webpages/exam/manager.html")


def list(request):
    draw = int(request.GET.get("draw", 1))
    start = int(request.GET.get("start", 0))
    length = int(request.GET.get("length", 10))
    search_value = request.GET.get("search[value]", "")
    order_column = int(request.GET.get("order[0][column]", 0))
    order_dir = request.GET.get("order[0][dir]", "asc")
    
    order_columns = {
        0: 'id',
        1: 'exam__title',
        2: 'subject__subject_name',
        3: 'duration',
        4: 'created'
    }
    
    order_field = order_columns.get(order_column, 'id')
    if order_dir == 'desc':
        order_field = '-' + order_field
    
    exam = Exam.objects.filter(is_deleted=False) 
    
    if search_value:
        exam = exam.filter(
            Q(created__icontains=search_value)|
            Q(subject__subject_name__icontains=search_value) |
            Q(duration__icontains=search_value)|
            Q(title__icontains=search_value)
        )
    
    total_records = exam.count()

    exam = exam.order_by(order_field)
    paginator = Paginator(exam, length)
    page_number = (start // length) + 1
    page_obj = paginator.get_page(page_number)

    data = []
    for exam in page_obj:
        
        
        
        data.append({
            "id": exam.id,
            "title": exam.title if exam.title else "N/A",
             "subject": exam.subject.subject_name if exam.subject.subject_name else "N/A",
            "duration": exam.duration if exam.duration else "N/A",
            "created": exam.created.strftime('%Y-%m-%d %H:%M')
        })
    
    response = {
        "draw": draw,
        "recordsTotal": total_records,
        "recordsFiltered": total_records,
        "data": data,
    }

    return JsonResponse(response)




def add(request):
    if request.method == 'POST':
        form = ExamForm(request.POST)  
        if form.is_valid():
           
            form.save()
            messages.success(request, "Question added successfully.")
            return redirect('dashboard-exam-manager')  
        else:
            return render(request, 'dashboard/webpages/exam/add.html', {'form': form})

    else:
        form = ExamForm()  

    return render(request, 'dashboard/webpages/exam/add.html', {'form': form})




def update(request, pk):
    exam = get_object_or_404(Exam, pk=pk)

    if request.method == 'POST':
        form = ExamForm(request.POST, instance=exam)
        if form.is_valid():
            form.save()
            messages.success(request, "Exam updated successfully.")
            return redirect('dashboard-exam-manager') 
        else:
            messages.error(request, "Failed to update exam. Please check the form for errors.")
    else:
        form = ExamForm(instance=exam)
    

    return render(request, 'dashboard/webpages/exam/update.html', {'form': form})




def delete(request, pk):
    exam = get_object_or_404(Exam, pk=pk)

    if request.method == 'POST':
        exam.is_deleted = True
        exam.save()
        messages.success(request, "Exam deleted successfully.")
        return redirect('dashboard-exam-manager')  
    messages.error(request, "Failed to delete exam.")
    return render(request, 'dashboard/webpages/exam/manager', {'exam': exam})