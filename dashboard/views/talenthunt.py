from django.shortcuts import redirect, render , get_object_or_404
from dashboard.models import *
from django.contrib import  messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from dashboard.models import CustomUser
from dashboard.forms.talenthunt import TalentHuntForm
from django.db.models import Q


def manager(request):
    return render (request,'dashboard/webpages/talenthunt/manager.html')



def list(request):
    
    draw = int(request.GET.get("draw", 1))
    start = int(request.GET.get("start", 0))
    length = int(request.GET.get("length", 10))  
    search_value = request.GET.get("search[value]", "")
    order_column = int(request.GET.get("order[0][column]", 0))
    order_dir = request.GET.get("order[0][dir]", "desc")
    

    order_columns = {
        0: 'id',
        1: 'subject_name',
        2: 'description',
        3:'course',
        # 4: 'created',
    }
    
    order_field = order_columns.get(order_column, 'id')
    if order_dir == 'desc':
        order_field = '-' + order_field
    
    talenthunt = TalentHunt.objects.filter(is_deleted=False)
    
    if search_value:
        talenthunt = talenthunt.filter(
            Q(subject_name__icontains=search_value)|
            Q(description__icontains=search_value)|
            Q(course__course_name__icontains=search_value)|
            Q(created__icontains=search_value)
        )
    
    total_records = talenthunt.count()

    talenthunt = talenthunt.order_by(order_field)
    paginator = Paginator(talenthunt, length)
    page_number = (start // length) + 1
    page_obj = paginator.get_page(page_number)

    data = []
    for talenthunt in page_obj:
        data.append({
            "id": talenthunt.id,
            "title":talenthunt.title if  talenthunt.title else "N/A",
            "course": talenthunt.course.course_name if talenthunt.course.course_name else "N/A",
            # "created": talenthunt.created.strftime('%Y-%m-%d %I:%M %p')
            "created": timezone.localtime(talenthunt.created).strftime('%Y-%m-%d %H:%M:%S')
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
        form = TalentHuntForm(request.POST, request.FILES)
        if form.is_valid():
            talenthunt = form.save(commit=False)
            course= form.cleaned_data.get('course')
            talenthunt.course = course

            talenthunt.save()

            
            messages.success(request, "TalenHunt added successfully!")
            return redirect('dashboard-talenthunt-manager')
        else:
            context = {
                "title": "Add Subject",
                "form": form,
            }
            return render(request, "dashboard/webpages/talenthunt/add.html", context)
    else:
            form = TalentHuntForm()  
            context = {
                "title": "Add talenthunt ",
                "form": form,
            }
            return render(request, "dashboard/webpages/talenthunt/add.html", context)

def update(request, pk):
    talenthunt = get_object_or_404(TalentHunt, pk=pk, is_deleted=False)

    if request.method == "POST":
        form = TalentHuntForm(request.POST, request.FILES, instance=talenthunt)  
        if form.is_valid():
            talenthunt = form.save(commit=False)
            course = form.cleaned_data.get('course')
            talenthunt.course = course

            talenthunt.save()

            messages.success(request, "TalenHunt updated successfully!")
            return redirect('dashboard-talenthunt-manager')
        else:
            context = {
                "title": "Update Subject",
                "form": form,
                "talenthunt": talenthunt,  
            }
            return render(request, "dashboard/webpages/talenthunt/update.html", context)
    else:
        form = TalentHuntForm(instance=talenthunt)  
        context = {
            "title": "Update Subject",
            "form": form,
            "talenthunt": talenthunt,  
        }
        return render(request, "dashboard/webpages/talenthunt/update.html", context)


def delete(request, pk):
    if request.method == "POST":
        talenthunt = get_object_or_404(TalentHunt, pk=pk, is_deleted=False)

        talenthunt.is_deleted = True
        talenthunt.save()

        messages.success(request, "TalenHunt deleted successfully!")
        return redirect('dashboard-talenthunt-manager')
    else:
        messages.error(request, "Invalid request method.")
        return redirect('dashboard-talenthunt-manager')







def fetch_course_subjects(request):
    course_id = request.GET.get('course_id')
    if course_id:
        subjects = Subject.objects.filter(course_id=course_id, is_deleted=False)
        subjects_data = [{'id': subject.id, 'name': subject.subject_name} for subject in subjects]
        return JsonResponse({'subjects': subjects_data})
    else:
        return JsonResponse({'subjects': []}, status=400) 
    






