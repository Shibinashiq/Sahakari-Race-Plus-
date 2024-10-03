from dashboard.views.imports import *

@api_view(['GET'])
def comment_list(request):
    video_id = request.GET.get('video_id')

    if not video_id:
        return Response({"status": "error", "message": "Either video_id or pdf_note_id is required"}, status=status.HTTP_400_BAD_REQUEST)

    comments = Comment.objects.filter(video_id=video_id, is_deleted=False).select_related('user')

    comment_data = []
    for comment in comments:
        formatted_date = comment.created.strftime('%Y-%m-%d %H:%M')
        comment_info = {
            'id': comment.id,
            'user_id': comment.user.id,
            'username': comment.user.name,  
            'user_image': comment.user.image.url if comment.user.image else None,  
            'content': comment.content,
            'created': formatted_date
        }
        comment_data.append(comment_info)

    return Response({"status": "success", "data": comment_data}, status=status.HTTP_200_OK)







@api_view(['POST'])
@login_required 
def comment_add(request):
    video_id = request.data.get('video_id')
    content = request.data.get('content')

    if not video_id or not content:
        return Response({"status": "error", "message": "Both video_id and content are required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        video = Video.objects.get(id=video_id)

        comment = Comment.objects.create(
            user=request.user, 
            video=video,
            content=content
        )

        response_data = {
            'id': comment.id,
            'user_id': comment.user.id,
            'username': comment.user.username,
            'user_image': comment.user.image.url if comment.user.image else None,
            'content': comment.content,
            'created': comment.created.strftime('%Y-%m-%d %H:%M:%S')  
        }

        return Response({"status": "success", "data": response_data}, status=status.HTTP_201_CREATED)

    except Video.DoesNotExist:
        return Response({"status": "error", "message": "Video not found."}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({"status": "error", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
