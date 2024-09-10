
from dashboard.views.imports import *


@login_required(login_url='dashboard-login')
def manager(request):
    return render(request, "dashboard/webpages/chapter/manager.html")




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
        1: 'chapter_name',
        2: 'description',
        3:'subject',
        # 4: 'created',
    }
    
    order_field = order_columns.get(order_column, 'id')
    if order_dir == 'desc':
        order_field = '-' + order_field
    
    chapters = Chapter.objects.filter(is_deleted=False).order_by('-id')
    
    if search_value:
        chapters = chapters.filter(
            Q(chapter_name__icontains=search_value)|
            Q(description__icontains=search_value)|
            Q(subject__subject_name__icontains=search_value)|
            Q(created__icontains=search_value)
        )
    
    total_records = chapters.count()

    chapters = chapters.order_by(order_field)
    paginator = Paginator(chapters, length)
    page_number = (start // length) + 1
    page_obj = paginator.get_page(page_number)

    data = []
    for chapter in page_obj:
        data.append({
            "id": chapter.id,
            "image": chapter.image.url if chapter.image else None,
            "chapter_name": chapter.chapter_name,
            "subject": chapter.subject.subject_name,
            "description": chapter.description,
            "created": timezone.localtime(chapter.created).strftime('%Y-%m-%d %H:%M:%S')

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
            form = ChapterForm(request.POST, request.FILES)
            if form.is_valid():
                chapter = form.save(commit=False)
                subject = form.cleaned_data.get('subject')
                chapter.subject = subject
                chapter.save()

               
                messages.success(request, "Chapter and subject information added successfully!")
                return redirect('dashboard-chapter')
            else:
                context = {
                    "title": "Add Chapter",
                    "form": form,
                }
                return render(request, "dashboard/webpages/chapter/add.html", context)
    else:
            form = ChapterForm()  
            context = {
                "title": "Add Chapter ",
                "form": form,
            }
            return render(request, "dashboard/webpages/chapter/add.html", context)

@login_required(login_url='dashboard-login')
def update(request, pk):
    chapter = get_object_or_404(Chapter, pk=pk)
    
    if request.method == "POST":
        form = ChapterForm(request.POST, request.FILES, instance=subject)
        if form.is_valid():
            chapter = form.save(commit=False)
            subject = form.cleaned_data.get('subject')
            chapter.subject = subject
            
            chapter.save()
            
            messages.success(request, "Chapter and subject information updated successfully!")
            return redirect('dashboard-subject')
        else:
            context = {
                "title": "Update Subject",
                "form": form,
            }
            return render(request, "dashboard/webpages/subject/update.html", context)
    else:
        form = ChapterForm(instance=subject)
        context = {
            "title": "Update Subject",
            "form": form,
        }
        return render(request, "dashboard/webpages/subject/update.html", context)
@login_required(login_url='dashboard-login')
def delete(request,pk):
    if request.method == "POST":
            chapter = get_object_or_404(Chapter, id=pk)
            chapter.is_deleted = True
            chapter.save()
            return JsonResponse({"message": "Chapter deleted successfully"})
     
    return JsonResponse({"message": "Invalid request"}, status=400)
     