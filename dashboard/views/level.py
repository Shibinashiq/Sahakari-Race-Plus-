
from dashboard.views.imports import *


@login_required(login_url='dashboard-login')
def manager(request,pk):
    context={
         'pk':pk
    }
    return render(request, 'dashboard/webpages/level/manager.html',context)



@login_required(login_url='dashboard-login')
def list(request,pk):

    draw = int(request.GET.get("draw", 1))
    start = int(request.GET.get("start", 0))
    length = int(request.GET.get("length", 10))  
    search_value = request.GET.get("search[value]", "")
    order_column = int(request.GET.get("order[0][column]", 0))
    order_dir = request.GET.get("order[0][dir]", "desc")
    

    order_columns = {
        0: 'id',
        3: 'course',

    }
    
    order_field = order_columns.get(order_column, 'id')
    if order_dir == 'desc':
        order_field = '-' + order_field
    
    level = Level.objects.filter(is_deleted=False,talenthuntsubject=pk)
    
    if search_value:
        level = level.filter(
            Q(title__icontains=search_value)|
            Q(number__icontains=search_value)|
            Q(created__icontains=search_value)
        )
    
    total_records = level.count()

    level = level.order_by(order_field)
    paginator = Paginator(level, length)
    page_number = (start // length) + 1
    page_obj = paginator.get_page(page_number)

    data = []
    for level in page_obj:
        data.append({
            "id": level.id,
            "title":level.title if  level.title else "N/A",
            "number": level.number if level.number else "N/A",
             "created": timezone.localtime(level.created).strftime('%Y-%m-%d %H:%M:%S')
        })
    
    response = {
        "draw": draw,
        "recordsTotal": total_records,
        "recordsFiltered": total_records,
        "data": data,
    }

    return JsonResponse(response)


@login_required(login_url='dashboard-login')
def add(request,pk):
    if request.method == "POST":
        talenthuntsubject= TalentHuntSubject.objects.get(id=pk)
        form = LevelForm(request.POST, request.FILES)
        if form.is_valid():
            level = form.save(commit=False)
            talenthuntsubject= form.cleaned_data.get('talenthuntsubject')
            level.talenthuntsubject = talenthuntsubject

            level.save()

            
            messages.success(request, "Level  added successfully!")
            return redirect('dashboard-level-manager',pk)
        else:
            context = {
                "title": "Add Subject",
                "form": form,
                "pk":pk,
            }
            return render(request, "dashboard/webpages/level/add.html", context)
    else:
            form = LevelForm()  
            context = {
                "title": "Add level ",
                "form": form,
                "pk":pk,
            }
            return render(request, "dashboard/webpages/level/add.html", context)
    


@login_required(login_url='dashboard-login')
def update(request, pk, level_id):
    talenthuntsubject = get_object_or_404(TalentHuntSubject, id=pk)
    level = get_object_or_404(Level, id=level_id, talenthuntsubject=talenthuntsubject)
    
    if request.method == "POST":
        form = LevelForm(request.POST, request.FILES, instance=level)
        if form.is_valid():
            form.save()
            messages.success(request, "Level updated successfully!")
            return redirect('dashboard-level-manager', pk)
        else:
            context = {
                "title": "Update Level",
                "form": form,
                "pk": pk,
                "level_id": level_id
            }
            return render(request, "dashboard/webpages/level/update.html", context)
    
    else:
        form = LevelForm(instance=level)
        context = {
            "title": "Update Level",
            "form": form,
            "pk": pk,
            "level_id": level_id
        }
        return render(request, "dashboard/webpages/level/update.html", context)
    

@login_required(login_url='dashboard-login')
def delete(request, pk):
    level = get_object_or_404(Level, id=pk)

    if request.method == "POST":
        level.is_deleted = True
        level.save()
        messages.success(request, "Level deleted successfully!")
        return redirect('dashboard-level-manager', pk)

    context = {
        "title": "Delete Level",
        "pk": pk,
    }
    return redirect('dashboard-level-question-manager',context)  




@login_required(login_url='dashboard-login')
def level_question_manager(request,pk):
    context={
         'pk':pk
    }
    return render(request, 'dashboard/webpages/level/question_manager.html',context)


@login_required(login_url='dashboard-login')
def level_question_list(request,pk):
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
    
    questions = Question.objects.filter(is_deleted=False,level=pk)
    
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
def level_question_add(request,pk):
    if request.method == 'POST':
        form = QuestionForm(request.POST)  
        if form.is_valid():
            level=Level.objects.get(id=pk,is_deleted=False)
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
                level=level

            )
           

            question.save()
            messages.success(request, "Question added successfully.")
            return redirect('dashboard-level-question-manager',pk)  
        else:
            return render(request, 'dashboard/webpages/level/question_add.html', {'form': form ,'pk':pk})

    else:
        form = QuestionForm()  

    return render(request, 'dashboard/webpages/level/question_add.html', {'form': form ,'pk':pk})



@login_required(login_url='dashboard-login')
def level_question_update(request,pk):
    question = get_object_or_404(Question, id=pk)
    
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
            return redirect('dashboard-level-question-manager',pk=question.level.id)  
    else:
        form = QuestionForm(instance=question)
    
    return render(request, 'dashboard/webpages/level/question_update.html', {
        'form': form,
        'question': question,
        'options': question.options,
        'answers': question.right_answers
    })


@login_required(login_url='dashboard-login')
def level_question_delete(request,pk):
    question = get_object_or_404(Question, id=pk)

    if request.method == "POST":
        question.is_deleted = True
        question.save()
        messages.success(request, "Question deleted successfully!")
        return redirect('dashboard-level-question-manager',pk=question.level.id)  
   
    return redirect('dashboard-level-question-manager',pk=question.level.id)  



@login_required(login_url='dashboard-login')
@csrf_exempt  
def paste(request):
    if request.method == 'POST':
        ids_json = request.POST.get('ids')
        level_id = request.POST.get('level_id')
        
        print(ids_json, level_id)

        try:
            level = Level.objects.get(id=level_id, is_deleted=False)
        except Level.DoesNotExist:
            return JsonResponse({'error': 'Level does not exist.'}, status=404)

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
                
                if Question.objects.filter(level=level, master_question=i, is_deleted=False).exists() or \
                   Question.objects.filter(level=level, id=master_question.master_question, is_deleted=False).exists() or \
                   Question.objects.filter(level=level, id=i, is_deleted=False).exists():
                    already_exists.append(i)
                    continue

                question = Question.objects.create(
                    question_type=master_question.question_type,
                    question_description=master_question.question_description,
                    hint=master_question.hint,
                    options=master_question.options,
                    right_answers=master_question.right_answers,
                    level=level,
                )
                
                question.master_question = master_question.master_question or i
                question.save()

                success_count += 1
            except ObjectDoesNotExist:
                error_messages.append(f"Master question with ID {i} does not exist.")
            except Exception as e:
                error_messages.append(f"Error creating question with ID {i}: {str(e)}")

        if success_count == 0 and not already_exists:
            return JsonResponse({'message': 'No questions were created.', 'errors': error_messages}, status=400)

        response_data = {
            'message': f'Successfully added {success_count} question(s) to the level.',
            'errors': error_messages,
        }
        if already_exists:
            response_data['existing'] = f"The following questions already existed in the level: {', '.join(map(str, already_exists))}"

        return JsonResponse(response_data, status=200)

    return JsonResponse({'error': 'Invalid request method.'}, status=405)
