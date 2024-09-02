from django.shortcuts import redirect, render , get_object_or_404
from dashboard.models import *
from django.contrib import  messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from dashboard.models import CustomUser
from dashboard.forms.question import QuestionForm
from django.db.models import Q


def add(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)  # Initialize form with POST data
        if form.is_valid():
            # Extract data from the form
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