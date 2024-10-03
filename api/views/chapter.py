from dashboard.views.imports import *
from api.serializers.chapter import ChapterSerializer



@api_view(['GET'])
def chapter_list(request):
    subject_id = request.GET.get('subject_id')
    
    if not subject_id:
        return Response({"status": "error", "message": "Subject ID is required"}, status=status.HTTP_400_BAD_REQUEST)

    chapters = Chapter.objects.filter(is_deleted=False, subject_id=subject_id)

    if chapters.exists():
        serializer = ChapterSerializer(chapters, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
    else:
        return Response({"status": "error", "message": "No chapters found for this subject"}, status=status.HTTP_404_NOT_FOUND)