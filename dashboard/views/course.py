from django.shortcuts import redirect, render , get_object_or_404
from dashboard.models import *
from dashboard.forms.course import AddForm
from dashboard.forms.subject import SubjectForm

from django.contrib import auth, messages
from django.http import JsonResponse
from django.core.paginator import Paginator

#course management

def manager(request):
        search = request.GET.get("search", '')
        if search == '':
            courses = Course.objects.filter(is_deleted=False).order_by('course_name')
        else:
            courses = Course.objects.filter(course_name__icontains=search, is_deleted=False).order_by('course_name')
        batches = Batch.objects.filter(course__in=courses, is_deleted=False)
        print(batches)

        context = {
            "title": " Courses ",
            "form": AddForm(),
            "courses": courses,
            "batches": batches,
        }
        return render(request, "dashboard/webpages/course/manager.html", context)
   


def add(request):
        if request.method == "POST":
            form = AddForm(request.POST, request.FILES)
            if form.is_valid():
                course = form.save(commit=False)

                course_fee = form.cleaned_data.get('course_fee')
                course_expire = form.cleaned_data.get('course_expire')

                course.save()

                Batch.objects.create(
                    course=course,
                    batch_price=course_fee,
                    batch_expiry=course_expire
                )

                messages.success(request, "Course and Batch information added successfully!")
                return redirect('dashboard-course')
            else:
                context = {
                    "title": "Add Course | Dashboard",
                    "form": form,
                }
                return render(request, "dashboard/webpages/course/manager.html", context)
        else:
            form = AddForm()  
            context = {
                "title": "Add Course | Agua Dashboard",
                "form": form,
            }
            return render(request, "dashboard/webpages/course/manager.html", context)



def update(request, pk):
    course = Course.objects.get(id=pk, is_deleted=False)
    if not course:
        messages.error(request, 'Course not found')
        return redirect('dashboard-course')

    try:
        batch = Batch.objects.get(course=course, is_deleted=False)
    except Batch.DoesNotExist:
        batch = None

    if request.method == 'POST':
        form = AddForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            course = form.save(commit=False)
            course_fee = form.cleaned_data.get('course_fee')
            course_expire = form.cleaned_data.get('course_expire')
            
            course.save()

            batch, created = Batch.objects.update_or_create(
                course=course,
                defaults={'batch_price': course_fee, 'batch_expiry': course_expire}
            )

            if created:
                messages.success(request, 'Batch created successfully')
            else:
                messages.success(request, 'Batch updated successfully')

            return redirect('dashboard-course')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        initial_data = {
            'course_fee': batch.batch_price if batch else 0.0,
            'course_expire': batch.batch_expiry if batch else None,
        }
        form = AddForm(instance=course, initial=initial_data)
    
    context = {
        "title": "Update Course | Agua Dashboard",
        "form": form,
        "course_id": course.id,
    }
    return render(request, "dashboard/includes/modals/update_in_modal.html", context)

def delete(request, pk):
		course = Course.objects.get(id = pk, is_deleted=False)
		course.is_deleted = True
		course.save()
		messages.success(request, 'Brand Deleted')
		return redirect('dashboard-course')


#subjects in course management

def course_subjects_list(request,pk):
     course = Course.objects.get(id=pk, is_deleted=False)
     context = {
         "title": "Subjects",
         "course": course,
     }
     return render(request,'dashboard/webpages/subject/manager.html',context)


def course_detail_subject(request, pk):
    draw = int(request.GET.get("draw", 1))
    start = int(request.GET.get("start", 0))
    length = int(request.GET.get("length", 10))  
    search_value = request.GET.get("search[value]", "")
    order_column = int(request.GET.get("order[0][column]", 0))
    order_dir = request.GET.get("order[0][dir]", "desc")
    
    course = get_object_or_404(Course, id=pk)

    order_columns = {
        0: 'id',
        1: 'subject_name',
        2: 'description',
        3: 'created',
    }
    
    order_field = order_columns.get(order_column, 'id')
    if order_dir == 'desc':
        order_field = '-' + order_field
    
    subjects = Subject.objects.filter(course=course, is_deleted=False)
    
    if search_value:
        subjects = subjects.filter(subject_name__icontains=search_value)
    
    total_records = subjects.count()

    subjects = subjects.order_by(order_field)
    paginator = Paginator(subjects, length)
    page_number = (start // length) + 1
    page_obj = paginator.get_page(page_number)

    data = []
    for subject in page_obj:
        data.append({
            "id": subject.id,
            "image": subject.image.url if subject.image else None,
            "subject_name": subject.subject_name,
            "description": subject.description,
            "created": subject.created.strftime('%Y-%m-%d %H:%M:%S')
        })
    
    response = {
        "draw": draw,
        "recordsTotal": total_records,
        "recordsFiltered": total_records,
        "data": data,
    }

    return JsonResponse(response)



def course_subject_add(request, pk):
    try:
        course = Course.objects.get(id=pk,is_deleted=False)
    except Course.DoesNotExist:
        messages.error(request, "Course not found.")
        return redirect('dashboard-course')

    if request.method == 'POST':
        form = SubjectForm(request.POST, request.FILES)
        if form.is_valid():
            subject = form.save(commit=False)
            subject.course = course  
            subject.save()
            messages.success(request, "Subject added successfully!")
            return redirect('dashboard-course-subjects-list', pk=pk)
        else:
            context = {
                "title": "Add Subject | Agua Dashboard",
                "form": form,
                "course": course,
            }

            return render(request, "dashboard/webpages/subject/manager.html", context)
    else:
        form = SubjectForm()
        context = {
            "title": "Add Subject | Agua Dashboard",
            "form": form,
            "course": course,
        }
        return render(request, "dashboard/webpages/subject/manager.html", context)





def course_subject_update(request, pk):
    print(pk,"{{{{{{{{{{{}}}}}}}}}}}")
    try:
        course = Course.objects.filter(id=pk,is_deleted=False)
    except Course.DoesNotExist:
        messages.error(request, "Course not found.")
        return redirect('dashboard-course')
    if request.method == 'POST':
        form = SubjectForm(request.POST, request.FILES)
        if form.is_valid():
            subject = form.save(commit=False)
            subject.course = course  
            subject.save()
            messages.success(request, "Subject added successfully!")
            return redirect('dashboard-course-subjects-list', pk=pk)
        else:
            context = {
                "title": "Update Subject | Agua Dashboard",
                "form": form,
                "course": course,
            }

            return render(request, "dashboard/webpages/subject/manager.html", context)
    else:
        form = SubjectForm()
        context = {
            "title": "Update Subject | Agua Dashboard",
            "form": form,
            "course": course,
        }
        return render(request, "dashboard/webpages/subject/manager.html", context)
    


def course_subject_delete(request, pk):
    try:
        subject = Subject.objects.get(id=pk, is_deleted=False)
        subject.is_deleted = True
        subject.save()  
        messages.success(request, 'Subject Deleted')
    except Subject.DoesNotExist:
        messages.error(request, 'Subject not found or already deleted.')

    return redirect('dashboard-course')