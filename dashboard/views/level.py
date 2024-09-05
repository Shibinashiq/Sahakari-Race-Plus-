
from django.shortcuts import redirect, render , get_object_or_404
from dashboard.models import *
from django.contrib import  messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from dashboard.models import CustomUser
from dashboard.forms.level import LevelForm ,QuestionForm
from django.db.models import Q

def manager(request,pk):
    context={
         'pk':pk
    }
    return render(request, 'dashboard/webpages/level/manager.html',context)




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
            "created": level.created.strftime('%Y-%m-%d %H:%M')
        })
    
    response = {
        "draw": draw,
        "recordsTotal": total_records,
        "recordsFiltered": total_records,
        "data": data,
    }

    return JsonResponse(response)



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





def level_question_manager(request,pk):
    context={
         'pk':pk
    }
    return render(request, 'dashboard/webpages/level/question_manager.html',context)



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
            "created": question.created.strftime('%Y-%m-%d %H:%M')
        })
    
    response = {
        "draw": draw,
        "recordsTotal": total_records,
        "recordsFiltered": total_records,
        "data": data,
    }

    return JsonResponse(response)

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

def level_question_delete(request,pk):
    question = get_object_or_404(Question, id=pk)

    if request.method == "POST":
        question.is_deleted = True
        question.save()
        messages.success(request, "Question deleted successfully!")
        return redirect('dashboard-level-question-manager',pk=question.level.id)  
   
    return redirect('dashboard-level-question-manager',pk=question.level.id)  
