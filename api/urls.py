
from django.urls import path
from django.contrib.auth import views as auth_views
from rest_framework_simplejwt import views as jwt_views
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
    path("v1/register/", authentication.register, name="api-v1-login"),
    path("v1/logout/", auth_views.LogoutView.as_view(), name="api-v1-logout"),
    path("v1/otp-auth/", authentication.otp_auth, name="api-v1-otp_auth"),
    path("v1/otp-login-verify/", authentication.otp_login_verify, name="api-v1-otp_login_verify"),
    path("v1/resend-otp/", authentication.resend_otp, name="api-v1-resend_otp"),
    path("v1/refresh-token/",jwt_views.TokenRefreshView.as_view(), name="api-v1-refresh_token"),

    
    # ==================================== Comment ============================================= #
    path('v1/update-profile/', student.update_profile, name='api-v1-update-profile'),

    # ==================================== Comment ============================================= #
    path('v1/course-list/', course.course_list, name='api-v1-course-list'),

    path('v1/subject-list/', subject.subject_list, name='api-v1-subject-list'),

    path('v1/chapter-list/', chapter.chapter_list, name='api-v1-chapter-list'),

    path('v1/lesson-list/', lesson.lesson_list, name='api-v1-lesson-list'),

    # ==================================== Comment ============================================= #
    path('v1/comment-list/', comment.comment_list, name='api-v1-comment-list'),
    path('v1/comment-add/', comment.comment_add, name='api-v1-comment-add'),

    # ==================================== Comment ============================================= #
    path('v1/comment-list/', comment.comment_list, name='api-v1-comment-list'),

 
]