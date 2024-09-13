from dashboard.views.imports import *

def manager(request):
    return render(request, 'dashboard/webpages/comment/manager.html')

def list(request):
    draw = int(request.GET.get("draw", 1))
    start = int(request.GET.get("start", 0))
    length = int(request.GET.get("length", 10))
    search_value = request.GET.get("search[value]", "").strip()
    order_column = int(request.GET.get("order[0][column]", 0))
    order_dir = request.GET.get("order[0][dir]", "desc")

    comments = Comment.objects.filter(is_deleted=False)

    order_columns = {
        0: 'id',
        1: 'user',
        2: 'content',
        3: 'created',
    }

    order_field = order_columns.get(order_column, 'id')
    if order_dir == 'desc':
        order_field = '-' + order_field

    if search_value:
        comments = comments.filter(
            Q(user__name__icontains=search_value) |
            Q(content__icontains=search_value)
        )

    total_records = comments.count()

    comments = comments.order_by(order_field)

    paginator = Paginator(comments, length)
    page_number = (start // length) + 1
    page_obj = paginator.get_page(page_number)

    data = []
    for comment in page_obj:
        # Collect video information if it exists
        video_data = {
            "video_url": comment.video.url if comment.video and comment.video.url else "N/A",
            "video_title": comment.video.title if comment.video and comment.video.title else "N/A",
            "video_is_free": comment.video.is_free if comment.video else False
        } if comment.video else None

        # Collect PDF note information if it exists
        pdf_note_data = {
            "pdf_title": comment.pdf_note.title if comment.pdf_note and comment.pdf_note.title else "N/A",
            "pdf_is_free": comment.pdf_note.is_free if comment.pdf_note else False,
            "pdf_file_url": comment.pdf_note.file.url if comment.pdf_note and comment.pdf_note.file else "N/A"
        } if comment.pdf_note else None

        # Add comment and related data
        data.append({
            "id": comment.id,
            "user": comment.user.name if comment.user.name else "N/A",
            "content": comment.content,
            "video": video_data,  # Include video data
            "pdf_note": pdf_note_data,  # Include PDF note data
            "created": timezone.localtime(comment.created).strftime('%Y-%m-%d %H:%M:%S'),
        })

    response = {
        "draw": draw,
        "recordsTotal": total_records,
        "recordsFiltered": total_records,
        "data": data,
    }

    return JsonResponse(response)




def delete(request,pk):
    try:
        comment = Comment.objects.get(id=pk)
        comment.is_deleted = True
        comment.save()
        messages.success(request, 'Comment deleted successfully')
    except Comment.DoesNotExist:
        messages.error(request, 'Comment not found')
    except Exception as e:
        messages.error(request, f'An error occurred: {str(e)}')
    
    return redirect('dashboard-comment-manager') 