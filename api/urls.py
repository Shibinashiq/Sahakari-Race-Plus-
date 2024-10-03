
from django.urls import path
from django.contrib.auth import views as auth_views
from api.views import (
  authentication,
  student,
  course,
  subject,
  chapter,
  lesson,

)

urlpatterns = [
    # ==================================== Authentication ============================================= #

    path("register/", authentication.register, name="api-v1-login"),
    path("logout/", auth_views.LogoutView.as_view(), name="api-v1-logout"),

    # ==================================== Student ============================================= #
    path('update-profile/', student.update_profile, name='api-v1-update-profile'),
 
    # ==================================== Course ============================================= #
    path('course-list/', course.course_list, name='api-v1-course-list'),

    # ==================================== Subject ============================================= #
    path('subject-list/', subject.subject_list, name='api-v1-subject-list'),

    # ==================================== chapter ============================================= #
    path('chapter-list/', chapter.chapter_list, name='api-v1-chapter-list'),


    # ==================================== Lesson ============================================= #
    path('lesson-list/', lesson.lesson_list, name='api-v1-lesson-list'),
 
]