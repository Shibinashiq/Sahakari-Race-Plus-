from dashboard.views.imports import *


@login_required(login_url='dashboard-login')
def manager(request):
    return render(request, "dashboard/webpages/success_stories/manager.html")


@login_required(login_url='dashboard-login')
def list(request):
    draw = int(request.GET.get("draw", 1))
    start = int(request.GET.get("start", 0))
    length = int(request.GET.get("length", 10))
    search_value = request.GET.get("search[value]", "").strip()
    order_column = int(request.GET.get("order[0][column]", 0))
    order_dir = request.GET.get("order[0][dir]", "desc")

    stories = SuccessStory.objects.filter(is_deleted=False)

    order_columns = {
        0: 'id',
        1: 'image',
        2: 'created_at',
    }

    order_field = order_columns.get(order_column, 'id')
    if order_dir == 'desc':
        order_field = '-' + order_field

    if search_value:
        stories = stories.filter(
            Q(title__icontains=search_value) |
            Q(description__icontains=search_value) 
        )

    total_records = stories.count()

    stories = stories.order_by(order_field)

    paginator = Paginator(stories, length)
    page_number = (start // length) + 1
    page_obj = paginator.get_page(page_number)

    data = []
    for story in page_obj:
        data.append({
            "id": story.id,
            "image": story.image.url if story.image else "N/A",
            "created": timezone.localtime(story.created_at).strftime('%Y-%m-%d %H:%M:%S'),
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
        form = SuccessStoriesForm(request.POST, request.FILES)
        if form.is_valid():
            success_story = form.save(commit=False)
            success_story.save()

            messages.success(request, "Success story added successfully!")
            return redirect('dashboard-success-stories-manager')
        else:
            context = {
                "title": "Add Success Story | Dashboard",
                "form": form,
            }
            return render(request, "dashboard/webpages/success_stories/add.html", context)
    else:
        form = SuccessStoriesForm()  
        context = {
            "title": "Add Success Story",
            "form": form,
        }
        return render(request, "dashboard/webpages/success_stories/add.html", context)
    


@login_required(login_url='dashboard-login')
def update(request, pk):
    success_story = get_object_or_404(SuccessStory, pk=pk)
    
    if request.method == "POST":
        form = SuccessStoriesForm(request.POST, request.FILES, instance=success_story)
        if form.is_valid():
            form.save()
            messages.success(request, "Success story updated successfully!")
            return redirect('dashboard-success-stories-manager')  
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = SuccessStoriesForm(instance=success_story)

    context = {
        "title": "Update Success Story",
        "form": form,
        "success_story": success_story
    }

    return render(request, "dashboard/webpages/success_stories/update.html", context)


@login_required(login_url='dashboard-login')
def delete(request, pk):
    if request.method == "POST":
        success_story = get_object_or_404(SuccessStory, pk=pk)
        success_story.is_deleted = True
        success_story.save()
        messages.success(request, "Success story deleted successfully!")
        return redirect('dashboard-success-stories-manager')
    else:
        messages.error(request, "Invalid request.")
        return redirect('dashboard-success-stories-manager')