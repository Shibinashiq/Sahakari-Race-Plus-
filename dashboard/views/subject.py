from django.shortcuts import redirect, render
from dashboard.models import *
from dashboard.forms.course import AddForm
from django.contrib import auth, messages


def manager (request):
    return render(request, "dashboard/webpages/subject/manager.html")


def subject_list(request):
    subjects = Subject.objects.all()
    return render(request, "dashboard/webpages/subject/list.html", {"subjects": subjects})





def add(reqeust):
    pass


def update(request):
    pass


def delete(request):
    pass