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
    
    user_filter = Lesson.objects.filter(is_deleted=False)
    
    if start_date and end_date:
        user_filter = user_filter.filter(created__range=[start_date, end_date])
 
    elif sort_option == 'name_ascending':
        user_list = user_filter.order_by('created')
    elif sort_option == 'name_descending':
        user_list = user_filter.order_by('-created')
    else:
        user_list = user_filter.order_by('-id')

    paginator = Paginator(user_list, 25)
    page_number = request.GET.get('page')
    users = paginator.get_page(page_number)

    staff_count = user_filter.count()
    folders = Folder.objects.filter(is_deleted=False,parent_folder=None,)
    context = {
        "lessons": users,
        "current_sort": sort_option,
        "start_date": start_date,
        "end_date": end_date,
        "staff_count": staff_count,
        "folders": folders,
    }


    return render(request, "ci/template/public/lesson/lesson.html", context)




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
            1: 'lesson_name',
            2: 'description',
            3: 'course',
            # 4: 'created',
        }
        
        order_field = order_columns.get(order_column, 'id')
        if order_dir == 'desc':
            order_field = '-' + order_field
        
        subjects = Lesson.objects.filter(is_deleted=False)
        
        if search_value:
            subjects = subjects.filter(
                Q(lesson_name__icontains=search_value)|
                Q(description__icontains=search_value)|
                Q(chapter__chapter_name__icontains=search_value)|
                Q(created__icontains=search_value)
            ) 
        
        total_records = subjects.count()

        subjects = subjects.order_by(order_field)
        paginator = Paginator(subjects, length)
        page_number = (start // length) + 1
        page_obj = paginator.get_page(page_number)

        data = []
        for lesson in page_obj:
            data.append({
                "id": lesson.id,
                "image": lesson.image.url if lesson.image else None,
                "lesson_name": lesson.lesson_name,
                "chapter": lesson.chapter.chapter_name,
                "description": lesson.description,
                "created": timezone.localtime(lesson.created).strftime('%Y-%m-%d %H:%M:%S')
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
            form = LessonForm(request.POST, request.FILES)
            if form.is_valid():
                lesson = form.save(commit=False)
                chapter = form.cleaned_data.get('chapter')
                visible_in_days = form.cleaned_data.get('visible_in_days')
                lesson.visible_in_days = visible_in_days
                lesson.chapter = chapter
                lesson.save()

                video_title = form.cleaned_data.get('video_title')
                video_url = form.cleaned_data.get('video_url')
                video_is_downloadable = form.cleaned_data.get('video_is_downloadable')
                video_is_free = form.cleaned_data.get('video_is_free')

                pdf_title = form.cleaned_data.get('pdf_title')
                pdf_file = form.cleaned_data.get('pdf_file')
                pdf_is_downloadable = form.cleaned_data.get('pdf_is_downloadable')
                pdf_is_free = form.cleaned_data.get('pdf_is_free')
                


                if video_url:
                    Video.objects.create(
                        lesson=lesson,
                        title=video_title,
                        url=video_url,
                        is_downloadable=video_is_downloadable,
                        is_free=video_is_free,
                    )
                if pdf_file is not None:
                    PDFNote.objects.create(
                        lesson=lesson,
                        title=pdf_title if pdf_title else None,
                        file=pdf_file,
                        is_downloadable=pdf_is_downloadable,
                        is_free=pdf_is_free,
                    )



            
               
                messages.success(request, "lesson and chapter information added successfully!")
                return redirect('dashboard-lesson')
            else:
                context = {
                    "title": "Add Lesson",
                    "form": form,
                }
                return render(request, "ci/template/public/lesson/add-lesson.html", context)
    else:
            form = LessonForm()  
            context = {
                "title": "Add Lesson ",
                "form": form,
            }
            return render(request, "ci/template/public/lesson/add-lesson.html", context)
    


@login_required(login_url='dashboard-login')    
def update(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)
    
    if request.method == "POST":
        form = LessonForm(request.POST, request.FILES, instance=lesson)
        if form.is_valid():
            lesson = form.save(commit=False)
            chapter = form.cleaned_data.get('chapter')
            visible_in_days = form.cleaned_data.get('visible_in_days')
            lesson.visible_in_days = visible_in_days
            lesson.chapter = chapter
            
            lesson.save()
            
            # Update or create video
            video_data = {
                'title': form.cleaned_data.get('video_title'),
                'url': form.cleaned_data.get('video_url'),
                'is_downloadable': form.cleaned_data.get('video_is_downloadable'),
                'is_free': form.cleaned_data.get('video_is_free'),
                'lesson': lesson,
            }
            Video.objects.update_or_create(lesson=lesson, defaults=video_data)
            
            pdf_data = {
                'title': form.cleaned_data.get('pdf_title'),
                'is_downloadable': form.cleaned_data.get('pdf_is_downloadable'),
                'is_free': form.cleaned_data.get('pdf_is_free'),
                'lesson': lesson,
            }
            if request.FILES.get('pdf_file'):
                pdf_data['file'] = request.FILES['pdf_file']
            PDFNote.objects.update_or_create(lesson=lesson, defaults=pdf_data)
            
            messages.success(request, "Lesson and chapter information updated successfully!")
            return redirect('dashboard-lesson')
        else:
            context = {
                "title": "Update Lesson",
                "form": form,
            }
            return render(request, "ci/template/public/lesson/update-lesson.html", context)
    else:
        form = LessonForm(instance=lesson)
        context = {
            "title": "Update Lesson",
            "form": form,
        }
        return render(request, "ci/template/public/lesson/update-lesson.html", context)
    

@login_required(login_url='dashboard-login')    
def delete(request, pk):
    if request.method == "POST":
            lesson = get_object_or_404(Lesson, id=pk)
            lesson.is_deleted = True
            lesson.save()
            return JsonResponse({"message": "lesson deleted successfully"})
     
    return JsonResponse({"message": "Invalid request"}, status=400)
     




