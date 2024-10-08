from dashboard.views.imports import *




#listing folder inside the folder
@login_required(login_url='dashboard-login')
def manager(request, folder_id):
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

    folders = Folder.objects.filter(parent_folder_id=folder_id, is_deleted=False)
    
    

    lessons = Lesson.objects.filter(folder=folder_id, is_deleted=False)

    if start_date and end_date:
        lessons = lessons.filter(created__range=[start_date, end_date])

    if sort_option == 'name_ascending':
        lessons = lessons.order_by('lesson_name')  
    elif sort_option == 'name_descending':
        lessons = lessons.order_by('-lesson_name')
    else:
        lessons = lessons.order_by('-id')  

    paginator = Paginator(lessons, 25)  
    page_number = request.GET.get('page')
    paginated_lessons = paginator.get_page(page_number)

    context = {
        "folder_id":folder_id,
        "folders": folders,  # Pass all folders
        "lessons": paginated_lessons,
        "current_sort": sort_option,
        "start_date": start_date,
        "end_date": end_date,
        "lesson_count": lessons.count(),  
    }

    return render(request, "ci/template/public/content/folder/folder.html", context)




#adding folder inside the lesson

@csrf_exempt
def add(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode("utf-8"))
        folder_name = data.get('folder_name')
        chapter_id = data.get('chapter_id', None)
        parent_id = data.get('parent_id', None)

        if not folder_name:
            return JsonResponse({'success': False, 'error': 'Folder name is required'})

        if chapter_id is not None and parent_id is None:
            try:
                chapter = Chapter.objects.get(id=chapter_id)
                folder = Folder.objects.create(title=folder_name, chapter=chapter)

                return JsonResponse({'success': True, 'folder_id': folder.id})
            except Chapter.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Chapter not found'})
        elif parent_id is not None:
            parent_folder = Folder.objects.get(id=parent_id)
            folder = Folder.objects.create(title=folder_name, parent_folder=parent_folder, chapter=parent_folder.chapter)
            return JsonResponse({'success': True, 'folder_id': folder.id})

        return JsonResponse({'success': False, 'error': 'Invalid request'})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})




@csrf_exempt  
def update(request):
    if request.method == "POST":
        try:
            # Parse JSON data from request body
            data = json.loads(request.body)
            folder_id = data.get('folder_id')
            new_folder_name = data.get('new_folder_name')
            print("hiiiiiiiiiiiiiii")
            print(folder_id)
            print(new_folder_name)

            if not folder_id or not new_folder_name:
                return JsonResponse({'success': False, 'error': 'Folder ID and new name are required.'})

            folder = get_object_or_404(Folder, pk=folder_id)

            folder.title = new_folder_name
            folder.save()

            return JsonResponse({'success': True})

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request method.'})


@csrf_exempt
def delete(request):
    if request.method == "POST":
        try:
            import json
            data = json.loads(request.body)
            folder_id = data.get('folder_id')

            if not folder_id:
                return JsonResponse({'success': False, 'error': 'Folder ID is required.'}, status=400)

            try:
                folder = Folder.objects.get(id=folder_id)
                folder.is_deleted = True
                folder.save()
                return JsonResponse({'success': True})

            except Folder.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Folder not found.'}, status=404)

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=405)



from dashboard.forms.content.lesson import LessonForm
def lesson_add(request,pk):
    try:
        chapter = Folder.objects.get(id=pk, is_deleted=False)
    except Folder.DoesNotExist:
        messages.error(request, "Folder not found.")
        return redirect('dashboard-course')
    

    if request.method == 'POST':
        form = LessonForm(request.POST, request.FILES)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.folder = chapter
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



            
            messages.success(request, "chapter added successfully!")
            return redirect('dashboard-folder', folder_id=pk)
    else:
        form = LessonForm()

    context = {
        "form": form,
        "chapter": pk,
    }
    return render(request, "ci/template/public/content/folder/add-lesson.html",context)




@login_required(login_url='dashboard-login')
def lesson_update(request, pk, folder_id):
    lesson = get_object_or_404(Lesson, id=pk, is_deleted=False)
    folder = get_object_or_404(Folder, id=folder_id, is_deleted=False)

    # Fetch existing Video and PDFNote related to the lesson
    video = Video.objects.filter(lesson=lesson).first()
    pdf = PDFNote.objects.filter(lesson=lesson).first()

    if request.method == 'POST':
        form = LessonForm(request.POST, request.FILES, instance=lesson)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.folder = folder
            lesson.save()

            video_title = form.cleaned_data.get('video_title')
            video_url = form.cleaned_data.get('video_url')
            video_is_downloadable = form.cleaned_data.get('video_is_downloadable')
            video_is_free = form.cleaned_data.get('video_is_free')

            # Update or create video
            if video_url:
                Video.objects.update_or_create(
                    lesson=lesson,
                    defaults={
                        'title': video_title,
                        'url': video_url,
                        'is_downloadable': video_is_downloadable,
                        'is_free': video_is_free,
                    }
                )

            pdf_title = form.cleaned_data.get('pdf_title')
            pdf_file = form.cleaned_data.get('pdf_file')
            pdf_is_downloadable = form.cleaned_data.get('pdf_is_downloadable')
            pdf_is_free = form.cleaned_data.get('pdf_is_free')

            # Update or create PDF
            if pdf_file is not None:
                PDFNote.objects.update_or_create(
                    lesson=lesson,
                    defaults={
                        'title': pdf_title if pdf_title else None,
                        'file': pdf_file,
                        'is_downloadable': pdf_is_downloadable,
                        'is_free': pdf_is_free,
                    }
                )

            messages.success(request, "Lesson updated successfully!")
            return redirect('dashboard-folder', folder_id=folder_id)
    else:
        # Prepopulate form with existing video and PDF data
        initial_data = {
            'video_title': video.title if video else '',
            'video_url': video.url if video else '',
            'video_is_downloadable': video.is_downloadable if video else False,
            'video_is_free': video.is_free if video else False,
            'pdf_title': pdf.title if pdf else '',
            'pdf_file': pdf.file if pdf else None,
            'pdf_is_downloadable': pdf.is_downloadable if pdf else False,
            'pdf_is_free': pdf.is_free if pdf else False,
        }

        form = LessonForm(instance=lesson, initial=initial_data)

    context = {
        "title": "Update Lesson",
        "form": form,
    }
    return render(request, "ci/template/public/content/folder/update-lesson.html", context)





@login_required(login_url='dashboard-login')
def lesson_delete(request, folder_id, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)

    lesson.is_deleted = True
    lesson.save()

    return redirect('dashboard-folder', folder_id=folder_id)
