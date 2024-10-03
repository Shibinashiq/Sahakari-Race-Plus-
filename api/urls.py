
from django.urls import path
from django.contrib.auth import views as auth_views
from api.views import (
  authentication,
  student,
  course,
  subject,
  chapter,
  lesson,
  comment,

)

urlpatterns = [
    # ==================================== Comment ============================================= #
    path("register/", authentication.register, name="api-v1-login"),
    path("logout/", auth_views.LogoutView.as_view(), name="api-v1-logout"),

    # ==================================== Comment ============================================= #
    path('update-profile/', student.update_profile, name='api-v1-update-profile'),

    # ==================================== Comment ============================================= #
    path('course-list/', course.course_list, name='api-v1-course-list'),

    path('subject-list/', subject.subject_list, name='api-v1-subject-list'),

    path('chapter-list/', chapter.chapter_list, name='api-v1-chapter-list'),

    path('lesson-list/', lesson.lesson_list, name='api-v1-lesson-list'),

    # ==================================== Comment ============================================= #
    path('comment-list/', comment.comment_list, name='api-v1-comment-list'),
    path('comment-add/', comment.comment_add, name='api-v1-comment-add'),

    # ==================================== Comment ============================================= #
    path('comment-list/', comment.comment_list, name='api-v1-comment-list'),

 
]