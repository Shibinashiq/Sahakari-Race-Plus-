from dashboard.views.imports  import *
from api.serializers.subject import SubjectSerializer




@api_view(['GET'])
def subject_list(request):
    course_id = request.GET.get('course_id')
    
    if not course_id:
        return Response({"status": "error", "message": "Course ID is required"}, status=status.HTTP_400_BAD_REQUEST)

    subjects = Subject.objects.filter(is_deleted=False, course_id=course_id)
    
    if subjects.exists():
        serializer = SubjectSerializer(subjects, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
    else:
        return Response({"status": "error", "message": "No subjects found for this course"}, status=status.HTTP_404_NOT_FOUND)