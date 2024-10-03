from dashboard.views.imports import *
from api.serializers.course  import CourseSerializer


@api_view(["POST"])
@permission_classes([IsAuthenticated]) 
def course_list(request):
    courses = Course.objects.filter(is_deleted=False)

    serializer = CourseSerializer(courses, many=True)

    response = {
        "status": "success",
        "message": "Courses retrieved successfully",
        "courses": serializer.data,  
    }
    
    return Response(response, status=status.HTTP_200_OK)	