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
    
    

    lessons = Lesson.objects.filter(folder__in=folders, is_deleted=False)

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




def update(request,pk):
    pass


def delete(request,pk):
    pass



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






# @login_required(login_url='dashboard-login')
# def chapter_lesson_update(request, chapter_id, lesson_id):
#     chapter = get_object_or_404(Chapter, id=chapter_id, is_deleted=False)
#     lesson = get_object_or_404(Lesson, id=lesson_id, chapter=chapter, is_deleted=False)
#     if request.method == 'POST':
#         form = LessonForm(request.POST, request.FILES, instance=lesson)
#         if form.is_valid():
#             lesson = form.save(commit=False)
#             lesson.chapter = chapter  
#             lesson.save()

#             video_title = form.cleaned_data.get('video_title')
#             video_url = form.cleaned_data.get('video_url')
#             video_is_downloadable = form.cleaned_data.get('video_is_downloadable')
#             video_is_free = form.cleaned_data.get('video_is_free')

#             if video_url:
#                 Video.objects.update_or_create(
#                     lesson=lesson,
#                     defaults={
#                         'title': video_title,
#                         'url': video_url,
#                         'is_downloadable': video_is_downloadable,
#                         'is_free': video_is_free,
#                     }
#                 )

#             pdf_title = form.cleaned_data.get('pdf_title')
#             pdf_file = form.cleaned_data.get('pdf_file')
#             pdf_is_downloadable = form.cleaned_data.get('pdf_is_downloadable')
#             pdf_is_free = form.cleaned_data.get('pdf_is_free')

#             if pdf_file is not None:
#                 PDFNote.objects.update_or_create(
#                     lesson=lesson,
#                     defaults={
#                         'title': pdf_title if pdf_title else None,
#                         'file': pdf_file,
#                         'is_downloadable': pdf_is_downloadable,
#                         'is_free': pdf_is_free,
#                     }
#                 )

#             messages.success(request, "Lesson updated successfully!")
#             return redirect('dashboard-chapters-lesson-list', chapter_id=chapter.id)
#     else:
#         form = LessonForm(instance=lesson)

#     context = {
#         "title": "Update Lesson",
#         "form": form,
#         "chapter": chapter,
#     }
#     return render(request, "ci/template/public/content/lesson/update-lesson.html", context)







# @login_required(login_url='dashboard-login')
# def chapter_lesson_delete(request,chapter_id,lesson_id):
#     lesson = get_object_or_404(Lesson, id=lesson_id)
#     lesson.is_deleted = True
#     lesson.save()
#     return redirect('dashboard-chapters-lesson-list', chapter_id=chapter_id)
