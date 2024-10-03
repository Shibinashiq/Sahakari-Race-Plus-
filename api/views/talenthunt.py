from dashboard.views.imports import *

@api_view(['GET'])
def talenthunt_list(request):
    course_id = request.GET.get('course_id') 

    if not course_id:
        return Response({"status": "error", "message": "course_id is required."}, status=status.HTTP_400_BAD_REQUEST)

    course = get_object_or_404(Course, id=course_id)

    talent_hunts = TalentHunt.objects.filter(course=course, is_deleted=False).values('id', 'title')

    response_data = list(talent_hunts)

    return Response({"status": "success", "data": response_data}, status=status.HTTP_200_OK)




@api_view(['GET'])
def talenthunt_subject_list(request):
    talent_hunt_id = request.GET.get('talent_hunt_id') 

    if not talent_hunt_id:
        return Response({"status": "error", "message": "talent_hunt_id is required."}, status=status.HTTP_400_BAD_REQUEST)

    talent_hunt = get_object_or_404(TalentHunt, id=talent_hunt_id)

    talent_hunt_subjects = TalentHuntSubject.objects.filter(talentHunt=talent_hunt, is_deleted=False).select_related('subject')

    response_data = [
        {
            "id": th_subject.id,
            "title": th_subject.title,
            "subject_name": th_subject.subject.subject_name if th_subject.subject else None,  
            "created": th_subject.created.isoformat()
        }
        for th_subject in talent_hunt_subjects
    ]

    return Response({"status": "success", "data": response_data}, status=status.HTTP_200_OK)