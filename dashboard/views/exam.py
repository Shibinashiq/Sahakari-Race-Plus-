from dashboard.views.imports import *

@login_required(login_url='dashboard-login')
def manager(request):

    return render(request, "dashboard/webpages/exam/manager.html")

@login_required(login_url='dashboard-login')
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
            "subject": exam.subject.subject_name if exam.subject else "N/A",
            "duration": exam.duration if exam.duration else "N/A",
            "created": timezone.localtime(exam.created).strftime('%Y-%m-%d %H:%M:%S')
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



@login_required(login_url='dashboard-login')
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



@login_required(login_url='dashboard-login')
def delete(request, pk):
    exam = get_object_or_404(Exam, pk=pk)

    if request.method == 'POST':
        exam.is_deleted = True
        exam.save()
        messages.success(request, "Exam deleted successfully.")
        return redirect('dashboard-exam-manager')  
    messages.error(request, "Failed to delete exam.")
    return render(request, 'dashboard/webpages/exam/manager', {'exam': exam})










@login_required(login_url='dashboard-login')
def exam_question_manager(request, exam_id):
    exam = get_object_or_404(Exam, pk=exam_id)
    return render(request, 'dashboard/webpages/exam/exam_question_manager.html', {'exam': exam.id})



@login_required(login_url='dashboard-login')
def exam_question_list(request,exam_id):
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
        3: 'exam__title',
        4: 'created'
    }
    
    order_field = order_columns.get(order_column, 'id')
    if order_dir == 'desc':
        order_field = '-' + order_field
    
    questions = Question.objects.filter(is_deleted=False,exam=exam_id)
    
    if search_value:
        questions = questions.filter(
            Q(question_description__icontains=search_value) |
            Q(hint__icontains=search_value) |
            Q(exam__name__icontains=search_value)
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
            "created": question.created.strftime('%Y-%m-%d %H:%M')
        })
    
    response = {
        "draw": draw,
        "recordsTotal": total_records,
        "recordsFiltered": total_records,
        "data": data,
    }

    return JsonResponse(response)


@login_required(login_url='dashboard-login')
def exam_question_add(request, exam_id):
    exam=Exam.objects.get(id=exam_id,is_deleted=False)
    
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
                exam_id=exam.id
            )
            question.save()
            messages.success(request, "Question added successfully.")
            return redirect('dashboard-exam-question-manager',exam_id=exam_id)  
        else:
            return render(request, 'dashboard/webpages/exam/question_add.html', {'form': form ,'exam':exam_id})

    else:
        form = QuestionForm()  

    return render(request, 'dashboard/webpages/exam/question_add.html', {'form': form ,'exam':exam_id})


@login_required(login_url='dashboard-login')
def exam_question_update(request,exam_id,question_id):
    question = get_object_or_404(Question, pk=question_id)
    exam = Exam.objects.get(id=exam_id)
    
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
            question.exam = exam
            question.options = options
            question.right_answers = answers
            question.save()
            if question.master_question:
                master_question=Question.objects.get(id=question.master_question,is_deleted=False)
                master_question.question_type = question_type
                master_question.question_description = question_description
                master_question.hint = hint
                master_question.options = options
                master_question.right_answers = answers
                master_question.save()
            related_questions = Question.objects.filter(master_question=question.id, is_deleted=False)
            for related_question in related_questions:
                related_question.question_type = question_type
                related_question.question_description = question_description
                related_question.hint = hint
                related_question.options = options
                related_question.right_answers = answers
                related_question.save()

            messages.success(request, 'Question updated successfully.')
            return redirect('dashboard-exam-question-manager',exam_id=exam_id)  
    else:
        form = QuestionForm(instance=question)
    
    return render(request, 'dashboard/webpages/exam/question_update.html', {
        'form': form,
        'question': question,
        'options': question.options,
        'answers': question.right_answers
    })






@login_required(login_url='dashboard-login')
def exam_question_delete(request,exam_id,question_id):
    if request.method == 'POST':
        question = get_object_or_404(Question, pk=question_id)
        question.is_deleted = True
        question.save()
        messages.success(request, 'Question deleted successfully.')
        return redirect('dashboard-exam-question-manager',exam_id=exam_id)  
    messages.error(request, 'Failed to delete question.')
    return redirect('dashboard-exam-question-manager',exam_id=exam_id)  
   


@login_required(login_url='dashboard-login')
def paste(request):
    
    if request.method == 'POST':
        ids_json = request.POST.get('ids')
        exam_id = request.POST.get('exam_id')

        try:
            exam = Exam.objects.get(id=exam_id, is_deleted=False)
        except Exam.DoesNotExist:
            return JsonResponse({'error': 'Exam does not exist.'}, status=404)
        
        try:
            ids = json.loads(ids_json) if ids_json else []
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid IDs format. Must be valid JSON.'}, status=400)

        if not all(str(i).isdigit() for i in ids):
            return JsonResponse({'error': 'All IDs must be numeric.'}, status=400)

        success_count = 0
        error_messages = []
        already_exists = []
        

        for i in ids:
            try:
                master_question = Question.objects.get(id=i)
               
                
                if Question.objects.filter(exam=exam, master_question=i, is_deleted=False).exists() or \
                    Question.objects.filter(exam=exam, id=master_question.master_question, is_deleted=False).exists() or \
                    Question.objects.filter(exam=exam, id=i, is_deleted=False).exists():
                        already_exists.append(i)
                        continue
                   
                question=Question.objects.create(
                    question_type=master_question.question_type,
                    question_description=master_question.question_description,
                    hint=master_question.hint,
                    options=master_question.options,
                    right_answers=master_question.right_answers,
                    exam=exam,
                    
                )
                if master_question.master_question:
                    question.master_question = master_question.master_question
                question.master_question = i
                question.save()
                success_count += 1  
            except ObjectDoesNotExist:
                error_messages.append(f"Master question with ID {i} does not exist.")
            except Exception as e:
                error_messages.append(f"Error creating question with ID {i}: {str(e)}")

        if success_count == 0 and not already_exists:
            return JsonResponse({'error': 'No questions were created.', 'details': error_messages}, status=400)
        
        response_data = {
            'message': f'Successfully added {success_count} question(s) to the exam.',
            'errors': error_messages
        }
        if already_exists:
            response_data['existing'] = f"The following questions already existed in the exam: {', '.join(map(str, already_exists))}"

        return JsonResponse(response_data, status=200)

    return JsonResponse({'error': 'Invalid request method.'}, status=405)
