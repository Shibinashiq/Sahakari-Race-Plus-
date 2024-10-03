from dashboard.views.imports import *           
from api.serializers.lesson import FullLessonSerializer ,FolderSerializer,LessonSerializer ,NestedFolderSerializer



@api_view(['GET'])
def lesson_list(request):
    chapter_id = request.GET.get('chapter_id')

    if not chapter_id:
        return Response({"status": "error", "message": "Chapter ID is required"}, status=status.HTTP_400_BAD_REQUEST)

    all_folders = Folder.objects.filter(chapter_id=chapter_id, is_deleted=False)

    folder_data = []
    for folder in all_folders.filter(parent_folder=None): 
        folder_info = {
            'id': folder.id,
            'title': folder.title,
            'name': folder.name,
            'lessons': [],  
            'sub_folders': []  
        }

        lessons_in_folder = Lesson.objects.filter(folder=folder, is_deleted=False)

        for lesson in lessons_in_folder:
            lesson_info = {
                'id': lesson.id,
                'lesson_name': lesson.lesson_name,
                'image': lesson.image.url if lesson.image else None,
                'description': lesson.description,
                'videos': [], 
                'pdf_notes': []  
            }

            videos = lesson.videos.filter(is_deleted=False)
            for video in videos:
                video_info = {
                    'id': video.id,
                    'title': video.title,
                    'url': video.url,
                    'is_downloadable': video.is_downloadable,
                    'is_free': video.is_free
                }
                lesson_info['videos'].append(video_info)

            pdf_notes = lesson.pdf_notes.filter(is_deleted=False)
            for pdf_note in pdf_notes:
                pdf_note_info = {
                    'id': pdf_note.id,
                    'title': pdf_note.title,
                    'file': pdf_note.file.url if pdf_note.file else None,  
                    'is_downloadable': pdf_note.is_downloadable,
                    'is_free': pdf_note.is_free
                }
                lesson_info['pdf_notes'].append(pdf_note_info)

            folder_info['lessons'].append(lesson_info)

        sub_folders = all_folders.filter(parent_folder=folder)

        for sub_folder in sub_folders:
            sub_folder_info = {
                'id': sub_folder.id,
                'title': sub_folder.title,
                'name': sub_folder.name,
                'lessons': [],  
                'sub_folders': []  
            }

            lessons_in_sub_folder = Lesson.objects.filter(folder=sub_folder, is_deleted=False)

            for lesson in lessons_in_sub_folder:
                lesson_info = {
                    'id': lesson.id,
                    'lesson_name': lesson.lesson_name,
                    'image': lesson.image.url if lesson.image else None,
                    'description': lesson.description,
                    'videos': [],  
                    'pdf_notes': [] 
                }

                videos = lesson.videos.filter(is_deleted=False)
                for video in videos:
                    video_info = {
                        'id': video.id,
                        'title': video.title,
                        'url': video.url,
                        'is_downloadable': video.is_downloadable,
                        'is_free': video.is_free
                    }
                    lesson_info['videos'].append(video_info)

                pdf_notes = lesson.pdf_notes.filter(is_deleted=False)
                for pdf_note in pdf_notes:
                    pdf_note_info = {
                        'id': pdf_note.id,
                        'title': pdf_note.title,
                        'file': pdf_note.file.url if pdf_note.file else None,  
                        'is_downloadable': pdf_note.is_downloadable,
                        'is_free': pdf_note.is_free
                    }
                    lesson_info['pdf_notes'].append(pdf_note_info)

                sub_folder_info['lessons'].append(lesson_info)

            folder_info['sub_folders'].append(sub_folder_info)

        folder_data.append(folder_info)

    direct_lessons = Lesson.objects.filter(chapter_id=chapter_id, folder=None, is_deleted=False)

    direct_lessons_data = []
    for lesson in direct_lessons:
        direct_lessons_info = {
            'id': lesson.id,
            'lesson_name': lesson.lesson_name,
            'image': lesson.image.url if lesson.image else None,
            'description': lesson.description,
            'videos': [],  
            'pdf_notes': []  
        }

        videos = lesson.videos.filter(is_deleted=False)
        for video in videos:
            video_info = {
                'id': video.id,
                'title': video.title,
                'url': video.url,
                'is_downloadable': video.is_downloadable,
                'is_free': video.is_free
            }
            direct_lessons_info['videos'].append(video_info)

        pdf_notes = lesson.pdf_notes.filter(is_deleted=False)
        for pdf_note in pdf_notes:
            pdf_note_info = {
                'id': pdf_note.id,
                'title': pdf_note.title,
                'file': pdf_note.file.url if pdf_note.file else None, 
                'is_downloadable': pdf_note.is_downloadable,
                'is_free': pdf_note.is_free
            }
            direct_lessons_info['pdf_notes'].append(pdf_note_info)

        direct_lessons_data.append(direct_lessons_info)

    response_data = {
        'folders': folder_data, 
        'direct_lessons': direct_lessons_data  
    }

    return Response({"status": "success", "data": response_data}, status=status.HTTP_200_OK)
