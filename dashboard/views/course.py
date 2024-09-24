from django.shortcuts import redirect, render , get_object_or_404
from dashboard.models import *
from dashboard.forms.content.course import AddForm
from dashboard.forms.content.subject import SubjectForm
from dashboard.forms.content.chapter import ChapterForm
from dashboard.forms.content.lesson import LessonForm
from dashboard.forms.content.question import QuestionForm
from django.contrib import auth, messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from dashboard.views.imports  import *


@login_required(login_url='dashboard-login')
def manager(request):
    start_date = request.GET.get('start_date', None)
    end_date = request.GET.get('end_date', None)
    sort_option = request.GET.get('sort', 'name_ascending')  

    if start_date and start_date.lower() != 'null':
        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        except ValueError:
            start_date = None

    if end_date and end_date.lower() != 'null':
        try:
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date() + timedelta(days=1)  
        except ValueError:
            end_date = None

    level_filter = Course.objects.filter(is_deleted=False)

    if start_date and end_date:
        level_filter = level_filter.filter(created__range=[start_date, end_date])

    if sort_option == 'name_ascending':
        level_filter = level_filter.order_by('created')
    elif sort_option == 'name_descending':
        level_filter = level_filter.order_by('-created')
    # elif sort_option == 'date_ascending':
    #     level_filter = level_filter.order_by('created')
    # elif sort_option == 'date_descending':
    #     level_filter = level_filter.order_by('-created')

    paginator = Paginator(level_filter, 25)
    page_number = request.GET.get('page')
    levels_paginated = paginator.get_page(page_number)

    context = {
        'courses': levels_paginated,
        'start_date': start_date,
        'end_date': end_date,
        'current_sort': sort_option,
    }

    return render(request, 'ci/template/public/content/course/course.html', context)

@login_required(login_url='dashboard-login')
def add(request):
        if request.method == "POST":
            form = AddForm(request.POST, request.FILES)
            if form.is_valid():
                course = form.save(commit=False)

              
                course.save()

               
                messages.success(request, "Course and Batch information added successfully!")
                return redirect('dashboard-course')
            else:
                context = {
                    "title": "Add Course | Dashboard",
                    "form": form,
                }
                return render(request, "ci/template/public/content/course/add-course.html", context)
        else:
            form = AddForm()  
            context = {
                "title": "Add Course | Agua Dashboard",
                "form": form,
            }
            return render(request, "ci/template/public/content/course/add-course.html", context)


@login_required(login_url='dashboard-login')
def update(request, pk):
    course = Course.objects.get(id=pk, is_deleted=False)
    if not course:
        messages.error(request, 'Course not found')
        return redirect('dashboard-course')


    if request.method == 'POST':
        form = AddForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            course = form.save(commit=False)
          
            
            course.save()

           
            messages.success(request, "Course updated successfully!")
            return redirect('dashboard-course')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        
        form = AddForm(instance=course)
    
    context = {
        "title": "Update Course | Agua Dashboard",
        "form": form,
        "course_id": course.id,
    }
    return render(request, "ci/template/public/content/course/update-course.html", context)



@login_required(login_url='dashboard-login')
def delete(request, pk):
		course = Course.objects.get(id = pk, is_deleted=False)
		course.is_deleted = True
		course.save()
		messages.success(request, 'Brand Deleted')
		return redirect('dashboard-course')


#subjects in course management
@login_required(login_url='dashboard-login')
def course_subjects_list(request, pk):
    course = get_object_or_404(Course, id=pk, is_deleted=False)
    
    search_query = request.GET.get('search', '')
    start_date = request.GET.get('start_date', None)
    end_date = request.GET.get('end_date', None)
    sort_option = request.GET.get('sort', 'name_ascending')  

    subjects = Subject.objects.filter(is_deleted=False, course=course)

    if search_query:
        subjects = subjects.filter(subject_name__icontains=search_query)

    if start_date and start_date.lower() != 'null':
        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        except ValueError:
            start_date = None

    if end_date and end_date.lower() != 'null':
        try:
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date() + timedelta(days=1)  
        except ValueError:
            end_date = None

    if start_date and end_date:
        subjects = subjects.filter(created__range=[start_date, end_date])

    if sort_option == 'name_ascending':
        subjects = subjects.order_by('subject_name')
    elif sort_option == 'name_descending':
        subjects = subjects.order_by('-subject_name')
    else:
        subjects = subjects.order_by('-created')  

    paginator = Paginator(subjects, 25) 
    page_number = request.GET.get('page')
    paginated_subjects = paginator.get_page(page_number)

    context = {
        'course': course,
        'subjects': paginated_subjects,
        'search_query': search_query,
        'start_date': start_date,
        'end_date': end_date,
        'current_sort': sort_option,
    }

    return render(request, 'ci/template/public/content/subject/subject.html', context)

@login_required(login_url='dashboard-login')
def course_detail_subject(request, course_id):
        draw = int(request.GET.get("draw", 1))
        start = int(request.GET.get("start", 0))
        length = int(request.GET.get("length", 10))  
        search_value = request.GET.get("search[value]", "")
        order_column = int(request.GET.get("order[0][column]", 0))
        order_dir = request.GET.get("order[0][dir]", "desc")
        
        course = Course.objects.filter(id=course_id, is_deleted=False).first()
        # if not course

        order_columns = {
            0: 'id',
            1: 'subject_name',
            2: 'description',
            3: 'created',
        }
        
        order_field = order_columns.get(order_column, 'id')
        if order_dir == 'desc':
            order_field = '-' + order_field
        
        subjects = Subject.objects.filter(is_deleted=False,course=course)
        
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
                "created": timezone.localtime(subject.created).strftime('%Y-%m-%d %H:%M:%S')
            })
        
        response = {
            "draw": draw,
            "course": course.id,
            "recordsTotal": total_records,
            "recordsFiltered": total_records,
            "data": data,
        }

        return JsonResponse(response)


@login_required(login_url='dashboard-login')
def course_subject_add(request, course_id):
    print("Request Method:", request.method)
    print("Course ID:", course_id)
    try:
        
        course = Course.objects.get(id=course_id, is_deleted=False)
        print("Course:", course)
    except Course.DoesNotExist:
        messages.error(request, "Course not found.")
        return redirect('dashboard-course')

    if request.method == 'POST':
        form = SubjectForm(request.POST, request.FILES)
        if form.is_valid():
            subject = form.save(commit=False)
            subject.course = course  
            print("hiiiiiiiiiiiiii")
            subject.save()
            messages.success(request, "Subject added successfully!")
            return redirect('dashboard-course-subjects-list', pk=course_id)
    else:
        form = SubjectForm()

    context = {
        "form": form,
        "course": course,
    }
    return render(request, "ci/template/public/content/subject/add-subject.html",context)


@login_required(login_url='dashboard-login')
def course_subject_update(request, course_id, subject_id):
    try:
        course = Course.objects.get(id=course_id, is_deleted=False)
    except Course.DoesNotExist:
        messages.error(request, "Course not found.")
        return redirect('dashboard-course')

    if request.method == 'POST':
        if subject_id:
            subject = get_object_or_404(Subject, id=subject_id, course=course)
            form = SubjectForm(request.POST, request.FILES, instance=subject)
        else:
            form = SubjectForm(request.POST, request.FILES)
        if form.is_valid():
            subject = form.save(commit=False)
            subject.course = course
            subject.save()
            messages.success(request, "Subject updated successfully!")
            return redirect('dashboard-course-subjects-list', pk=course_id)
    else:
        if subject_id:
            subject = get_object_or_404(Subject, id=subject_id, course=course)
            form = SubjectForm(instance=subject)
        else:
            form = SubjectForm()

    context = {
        "title": "Update Subject ",
        "form": form,
        "course": course,
    }
    return render(request, "ci/template/public/content/subject/add-subject-update.html", context)
    

@login_required(login_url='dashboard-login')
def course_subject_delete(request, pk):
    try:
        subject = Subject.objects.get(id=pk, is_deleted=False)
        subject.is_deleted = True
        subject.save()  
        messages.success(request, 'Subject Deleted')
    except Subject.DoesNotExist:
        messages.error(request, 'Subject not found or already deleted.')

    return redirect('dashboard-course')





@login_required(login_url='dashboard-login')
def course_subject_chapters_list(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id, is_deleted=False)

    chapters = Chapter.objects.filter(subject=subject, is_deleted=False)

    start_date = request.GET.get('start_date', None)
    end_date = request.GET.get('end_date', None)

    if start_date:
        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            chapters = chapters.filter(created__gte=start_date)
        except ValueError:
            start_date = None

    if end_date:
        try:
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
            chapters = chapters.filter(created__lte=end_date)
        except ValueError:
            end_date = None

    context = {
        "subject_id": subject_id,
        "chapters": chapters,  
        "subject_name": subject.subject_name,
        "course": subject.course, 
        "start_date": start_date,
        "end_date": end_date,
    }

    return render(request, 'ci/template/public/content/chapter/chapter.html', context)


@login_required(login_url='dashboard-login')
def subject_detail_chapter(request, pk):
    draw = int(request.GET.get("draw", 1))
    start = int(request.GET.get("start", 0))
    length = int(request.GET.get("length", 10))  
    search_value = request.GET.get("search[value]", "")
    order_column = int(request.GET.get("order[0][column]", 0))
    order_dir = request.GET.get("order[0][dir]", "desc")
    
    subject = get_object_or_404(Subject, id=pk)

    order_columns = {
        0: 'id',
        1: 'subject_name',
        2: 'description',
        3: 'created',
    }
    
    order_field = order_columns.get(order_column, 'id')
    if order_dir == 'desc':
        order_field = '-' + order_field
    
    chapter = Chapter.objects.filter(subject=subject, is_deleted=False)
    
    if search_value:
        chapter = chapter.filter(chapter_name__icontains=search_value)
    
    total_records = chapter.count()

    chapter = chapter.order_by(order_field)
    paginator = Paginator(chapter, length)
    page_number = (start // length) + 1
    page_obj = paginator.get_page(page_number)

    data = []
    for chapter in page_obj:
        data.append({
            "id": chapter.id,
            "image": chapter.image.url if chapter.image else None,
            "chapter_name": chapter.chapter_name,
            "description": chapter.description,
             "created": timezone.localtime(chapter.created).strftime('%Y-%m-%d %H:%M:%S')
        })
    
    response = {
        "draw": draw,
        "subject": subject.id,
        "recordsTotal": total_records,
        "recordsFiltered": total_records,
        "data": data,
    }

    return JsonResponse(response)



@login_required(login_url='dashboard-login')
def subject_chapter_add(request, pk):
    try:
        subject = Subject.objects.get(id=pk, is_deleted=False)
    except Subject.DoesNotExist:
        messages.error(request, "Subject not found.")
        return redirect('dashboard-course')
    

    if request.method == 'POST':
        form = ChapterForm(request.POST, request.FILES)
        if form.is_valid():
            chapter = form.save(commit=False)
            chapter.subject = subject
            chapter.save()
            messages.success(request, "chapter added successfully!")
            return redirect('subject-chapters-list', subject_id=pk)
    else:
        form = ChapterForm()

    context = {
        "form": form,
        "subject": subject,
    }
    return render(request, "ci/template/public/content/chapter/add-chapter.html",context)


@login_required(login_url='dashboard-login')
def subject_chapter_update(request, chapter_id, subject_id):
    subject = get_object_or_404(Subject, id=subject_id, is_deleted=False)
    chapter = get_object_or_404(Chapter, id=chapter_id, subject=subject)

    if request.method == 'POST':
        form = ChapterForm(request.POST, request.FILES, instance=chapter)
        if form.is_valid():
            chapter = form.save(commit=False)
            chapter.subject = subject
            chapter.save()
            messages.success(request, "Chapter updated successfully!")
            
            return redirect('subject-chapters-list', subject_id=subject_id)
    else:
        form = ChapterForm(instance=chapter)

    context = {
        "title": "Update Chapter",
        "form": form,
        "subject": subject,
    }
    return render(request, "ci/template/public/content/chapter/update-chapter.html", context)




@login_required(login_url='dashboard-login')
def subject_chapter_delete(request,chapter_id, subject_id):
    try:
        subject = Chapter.objects.get(id=chapter_id, is_deleted=False)
        subject.is_deleted = True
        subject.save()  
        messages.success(request, 'Chapter Deleted')
    except Subject.DoesNotExist:
        messages.error(request, 'Chapter not found or already deleted.')

    return redirect('subject-chapters-list', subject_id=subject_id)







@login_required(login_url='dashboard-login')
def chapter_lesson_list(request, chapter_id):
    chapter = get_object_or_404(Chapter, id=chapter_id)
    lessons = Lesson.objects.filter(chapter=chapter, is_deleted=False)

    # Handle search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        lessons = lessons.filter(lesson_name__icontains=search_query)

    # Handle date range filtering
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')

    if start_date:
        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            lessons = lessons.filter(created__gte=start_date)
        except ValueError:
            start_date = None

    if end_date:
        try:
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date() + timedelta(days=1)
            lessons = lessons.filter(created__lt=end_date)
        except ValueError:
            end_date = None

    # Pagination
    paginator = Paginator(lessons, 25) 
    page_number = request.GET.get('page')
    paginated_lessons = paginator.get_page(page_number)

    context = {
        "title": "Lessons",
        "chapter": chapter_id,
        "obj_chapter": chapter,
        "lessons": paginated_lessons,
        "search_query": search_query,
        "start_date": start_date,
        "end_date": end_date,
    }
    return render(request, 'ci/template/public/content/lesson/lesson.html', context)


@login_required(login_url='dashboard-login')
def chapter_detail_lesson(request, pk):
    draw = int(request.GET.get("draw", 1))
    start = int(request.GET.get("start", 0))
    length = int(request.GET.get("length", 10))
    search_value = request.GET.get("search[value]", "")
    order_column = int(request.GET.get("order[0][column]", 0))
    order_dir = request.GET.get("order[0][dir]", "desc")
    
    chapter = get_object_or_404(Chapter, id=pk)

    order_columns = {
        0: 'id',
        1: 'subject_name',
        2: 'description',
        3: 'created',
    }
    
    order_field = order_columns.get(order_column, 'id')
    if order_dir == 'desc':
        order_field = '-' + order_field
    
    lessons = Lesson.objects.filter(chapter=chapter, is_deleted=False)
    if search_value:
        lessons = lessons.filter(lesson_name__icontains=search_value)
    
    total_records = lessons.count()

    lessons = lessons.order_by(order_field)
    paginator = Paginator(lessons, length)
    page_number = (start // length) + 1
    page_obj = paginator.get_page(page_number)

    data = []
    for lesson in page_obj:
        videos = Video.objects.filter(lesson=lesson, is_deleted=False)
        pdfs = PDFNote.objects.filter(lesson=lesson, is_deleted=False)
        
        video_data = []
        for video in videos:
            video_data.append({
                "video_url": video.url if video.url else "N/A",
                "video_title": video.title if video.title else "N/A",
                "video_is_free": video.is_free
            })

        pdf_data = []
        for pdf in pdfs:
            pdf_data.append({
                "pdf_title": pdf.title if pdf.title else "N/A",
                "pdf_is_free": pdf.is_free,
                "pdf_file": pdf.file.url if pdf.file else "N/A"
            })

        data.append({
            "id": lesson.id,
            "image": lesson.image.url if lesson.image else None,
            "chapter_name": chapter.chapter_name,
            "videos": video_data,
            "pdfs": pdf_data,
            "description": lesson.description,
              "created": timezone.localtime(lesson.created).strftime('%Y-%m-%d %H:%M:%S')
        })
    
    response = {
        "draw": draw,
        "chapter": chapter.id,
        "recordsTotal": total_records,
        "recordsFiltered": total_records,
        "data": data,
    }

    return JsonResponse(response)










@login_required(login_url='dashboard-login')
def chapter_lesson_add(request,pk):
    try:
        chapter = Chapter.objects.get(id=pk, is_deleted=False)
    except Chapter.DoesNotExist:
        messages.error(request, "Subject not found.")
        return redirect('dashboard-course')
    

    if request.method == 'POST':
        form = LessonForm(request.POST, request.FILES)
        if form.is_valid():
            lesson = form.save(commit=False)
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



            
            messages.success(request, "chapter added successfully!")
            return redirect('dashboard-chapters-lesson-list', chapter_id=chapter.id)
    else:
        form = LessonForm()

    context = {
        "form": form,
        "chapter": pk,
    }
    return render(request, "ci/template/public/content/lesson/add-lesson.html",context)






@login_required(login_url='dashboard-login')
def chapter_lesson_update(request, chapter_id, lesson_id):
    
    chapter = get_object_or_404(Chapter, id=chapter_id, is_deleted=False)
    lesson = get_object_or_404(Lesson, id=lesson_id, chapter=chapter, is_deleted=False)
    if request.method == 'POST':
        form = LessonForm(request.POST, request.FILES, instance=lesson)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.chapter = chapter  
            lesson.save()

            video_title = form.cleaned_data.get('video_title')
            video_url = form.cleaned_data.get('video_url')
            video_is_downloadable = form.cleaned_data.get('video_is_downloadable')
            video_is_free = form.cleaned_data.get('video_is_free')

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
            return redirect('dashboard-chapters-lesson-list', chapter_id=chapter.id)
    else:
        form = LessonForm(instance=lesson)

    context = {
        "title": "Update Lesson",
        "form": form,
        "chapter": chapter,
    }
    return render(request, "ci/template/public/content/lesson/update-lesson.html", context)







@login_required(login_url='dashboard-login')
def chapter_lesson_delete(request,chapter_id,lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    lesson.is_deleted = True
    lesson.save()
    return redirect('dashboard-chapters-lesson-list', chapter_id=chapter_id)



@login_required(login_url='dashboard-login')
def chapter_question_list(request, chapter_id):
    # Get questions related to the chapter
    questions = Question.objects.filter(is_deleted=False, chapter_id=chapter_id)

    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        questions = questions.filter(question_description__icontains=search_query)

    # Date filtering
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')

    if start_date:
        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            questions = questions.filter(created__gte=start_date)
        except ValueError:
            start_date = None

    if end_date:
        try:
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date() + timedelta(days=1)
            questions = questions.filter(created__lt=end_date)
        except ValueError:
            end_date = None

    paginator = Paginator(questions, 25) 
    page_number = request.GET.get('page')
    paginated_questions = paginator.get_page(page_number)

    context = {
        'chapter': chapter_id,
        'questions': paginated_questions,
        'search_query': search_query,
        'start_date': start_date,
        'end_date': end_date,
    }

    return render(request, 'ci/template/public/content/question/lesson-question.html', context)


@login_required(login_url='dashboard-login')
def chapter_detail_question(request,pk):
    draw = int(request.GET.get("draw", 1))
    start = int(request.GET.get("start", 0))
    length = int(request.GET.get("length", 10))
    search_value = request.GET.get("search[value]", "")
    order_column = int(request.GET.get("order[0][column]", 0))
    order_dir = request.GET.get("order[0][dir]", "desc")
    
    order_columns = {
        0: 'id',
        1: 'question_description',
        2: 'hint',
        3: 'created'
    }
    
    order_field = order_columns.get(order_column, 'id')
    if order_dir == 'desc':
        order_field = '-' + order_field
    
    questions = Question.objects.filter(is_deleted=False, chapter_id=pk)
    
    if search_value:
        questions = questions.filter(
            Q(question_description__icontains=search_value) |
            Q(hint__icontains=search_value) 
        )
    
    total_records = questions.count()

    questions = questions.order_by(order_field)
    paginator = Paginator(questions, length)
    page_number = (start // length) + 1
    page_obj = paginator.get_page(page_number)

    data = []
    for question in page_obj:
        options_str = ', '.join(filter(None, question.options)) if question.options else "N/A"
        right_answers_str = ', '.join(filter(None, question.right_answers)) if question.right_answers else "N/A"
        
        if options_str.strip() == "":
            options_str = "N/A"
        if right_answers_str.strip() == "":
            right_answers_str = "N/A"
        
        data.append({
            "id": question.id,
            "question_description": question.question_description if question.question_description else "N/A",
            "hint": question.hint if question.hint else "N/A",
            "options": options_str,
            "right_answers": right_answers_str,
            "created": timezone.localtime(question.created).strftime('%Y-%m-%d %H:%M:%S')
        })
    
    response = {
        "draw": draw,
        "recordsTotal": total_records,
        "recordsFiltered": total_records,
        "data": data,
    }

    return JsonResponse(response)



@login_required(login_url='dashboard-login')
def chapter_question_add(request, pk):
    chapter=Chapter.objects.get(id=pk,is_deleted=False)
    
    if request.method == 'POST':
        form = QuestionForm(request.POST)  
        if form.is_valid():
            question_type = form.cleaned_data.get('question_type')
            question_description = form.cleaned_data.get('question_description')
            hint = form.cleaned_data.get('hint')
            options = request.POST.getlist('options[]')
            answers = request.POST.getlist('answers[]')

            question = Question(
                question_type=question_type,
                question_description=question_description,
                hint=hint,
                options=options,
                right_answers=answers,
                chapter=chapter
            )
            question.save()
            messages.success(request, "Question added successfully.")
            return redirect('dashboard-chapter-question-list',chapter_id=pk)  
        else:
            return render(request, 'ci/template/public/content/question/add-lesson-question.html', {'form': form ,'lesson':pk})

    else:
        form = QuestionForm()  

    return render(request, 'ci/template/public/content/question/add-lesson-question.html', {'form': form ,'lesson':pk})




@login_required(login_url='dashboard-login')
def chapter_question_update(request,question_id,chapter_id):
    question = get_object_or_404(Question, id=question_id)
    chapter = Chapter.objects.get(id=chapter_id,is_deleted=False)
    
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)  
        if form.is_valid():
            question_type = form.cleaned_data.get('question_type')
            question_description = form.cleaned_data.get('question_description')
            hint = form.cleaned_data.get('hint')
            options = request.POST.getlist('options[]')
            answers = request.POST.getlist('answers[]')

            question.question_type = question_type
            question.question_description = question_description
            question.hint = hint
            question.options = options
            question.right_answers = answers
            question.chapter = chapter
            question.save()

            messages.success(request, "Question updated successfully.")
            return redirect('dashboard-chapter-question-list', chapter_id=chapter.id)  
        else:
            return render(request, 'dashboard/webpages/content/lesson/lesson_question_update.html', { 'form': form,
        'question': question,
        'options': question.options,
        'answers': question.right_answers})

    else:
        form = QuestionForm(instance=question)  

    return render(request, 'dashboard/webpages/content/lesson/lesson_question_update.html', {'form': form,
        'question': question,
        'options': question.options,
        'answers': question.right_answers})




@login_required(login_url='dashboard-login')
def chapter_question_delete(request,question_id, chapter_id):
    if request.method == 'POST':
        question = get_object_or_404(Question, id=question_id)
        question.is_deleted = True
        question.save()
        messages.success(request, "Question deleted successfully.")
        return redirect('dashboard-chapter-question-list', chapter_id=chapter_id)
    messages.error(request, "Failed to delete question.")
    return redirect('dashboard-chapter-question-list', chapter_id=chapter_id)
    