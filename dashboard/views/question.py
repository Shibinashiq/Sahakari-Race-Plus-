from django.shortcuts import redirect, render , get_object_or_404
from dashboard.models import *
from django.contrib import  messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from dashboard.models import CustomUser
from dashboard.forms.question import QuestionForm
from django.db.models import Q




def manager(request):
    return render(request, 'dashboard/webpages/question/manager.html')


def list(request):
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
        3: 'exam__name',
        4: 'created'
    }
    
    order_field = order_columns.get(order_column, 'id')
    if order_dir == 'desc':
        order_field = '-' + order_field
    
    questions = Question.objects.filter(is_deleted=False)
    
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
        data.append({
            "id": question.id,
            "question_description": question.question_description if question.question_description else "",
            "hint": question.hint if question.hint else "",
            "exam": question.exam.name if question.exam else None,
            "options": ', '.join(question.options) if question.options else "",
            "right_answers": ', '.join(question.right_answers) if question.right_answers else "",
            "created": question.created.strftime('%Y-%m-%d %H:%M')
        })
    
    response = {
        "draw": draw,
        "recordsTotal": total_records,
        "recordsFiltered": total_records,
        "data": data,
    }

    return JsonResponse(response)



def add(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)  
        if form.is_valid():
            question_type = form.cleaned_data.get('question_type')
            question_description = form.cleaned_data.get('question_description')
            hint = form.cleaned_data.get('hint')
            exam_id = form.cleaned_data.get('exam')
            options = request.POST.getlist('options[]')
            answers = request.POST.getlist('answers[]')
            print("Options:", options)
            print("answers",answers)

            question = Question(
                question_type=question_type,
                question_description=question_description,
                hint=hint,
                options=options,
                right_answers=answers,
                exam_id=exam_id
            )
            question.save()
            
            return redirect('dashboard-question-add')  
        else:
            return render(request, 'dashboard/webpages/question/add.html', {'form': form})

    else:
        form = QuestionForm()  

    return render(request, 'dashboard/webpages/question/add.html', {'form': form})




def update(request, pk):
    question = get_object_or_404(Question, pk=pk)
    
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question_type = form.cleaned_data.get('question_type')
            question_description = form.cleaned_data.get('question_description')
            hint = form.cleaned_data.get('hint')
            exam_id = form.cleaned_data.get('exam')
            options = request.POST.getlist('options[]')
            answers = request.POST.getlist('answers[]')
            print("Options:", options)
            print("Answers:", answers)

            question.question_type = question_type
            question.question_description = question_description
            question.hint = hint
            question.exam_id = exam_id
            question.options = options
            question.right_answers = answers
            question.save()
            
            return redirect('dashboard-question-list')  
    else:
        form = QuestionForm(instance=question)
    
    return render(request, 'dashboard/webpages/question/edit.html', {'form': form, 'question': question})
