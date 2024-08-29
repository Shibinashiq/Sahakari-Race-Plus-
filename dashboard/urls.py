"""
This module defines the URL patterns for the dashboard application in a Django web application.

The URL patterns cover various functionalities, including authentication, route management, salesman management, brand management, product management, customer management, warehouse management, vehicle management, user management, coupon booklet type management, coupon booklet management, order management, cashier log management, and reporting.

Each URL pattern is associated with a view function that handles the corresponding functionality. The view functions are defined in various submodules, such as `authentication`, `route`, `salesman`, `brand`, `product`, `customer`, `warehouse_manager`, `vehicle`, `user`, `coupon_booklet_type`, `coupon_booklet`, `order`, `cashier_log`, `report`, and `credit`.

The URL patterns provide a structured and organized way to access the different features of the dashboard application, making it easier to maintain and extend the application as needed.
"""
from django.urls import path
from django.contrib.auth import views as auth_views
from dashboard.views import (
    authentication,
    course,
    home,
    subject,
   
)

urlpatterns = [
    # ==================================== Course ============================================= #

    path("login/", authentication.login, name="dashboard-login"),
    path("logout/", auth_views.LogoutView.as_view(), name="dashboard-logout"),

    # ==================================== Course ============================================= #
    
    path("", home.home, name="dashboard-home"),

    # ==================================== Course ============================================= #

    path("course/", course.manager, name="dashboard-course"),
    path("course/add/", course.add, name="dashboard-course-add"),
    path("course/update/<int:pk>/", course.update, name="dashboard-course-update"),
    path("course/delete/<int:pk>/", course.delete, name="dashboard-course-delete"),


    #subjects inside the course
    path("course/subject/list/<int:pk>/", course.course_subjects_list, name="dashboard-course-subjects-list"), #here list the subjects
    path("course/detail/<int:course_id>/", course.course_detail_subject, name="dashboard-course-detail"), #this endpoint fetch the subjects inside the course
    path("course/subject/add/<int:course_id>/", course.course_subject_add, name="dashboard-course-subject-add"),
    path("course/subject/update/<int:course_id>/<int:subject_id>/", course.course_subject_update, name="dashboard-course-subject-update"),
    path("course/subject/delete/<int:pk>/", course.course_subject_delete, name="dashboard-course-subject-delete"),


    #chapter inside the subject
    path("subject/chapter/list/<int:subject_id>/", course.course_subject_chapters_list, name="subject-chapters-list"), #here list the chapters
    path("subject/chapter/detail/<int:pk>/", course.subject_detail_chapter, name="dashboard-subject-chapters-detail"),
    path("subject/chapter/add/<int:pk>/", course.subject_chapter_add, name="dashboard-subject-chapter-add"),
    path("subject/chapter/update/<int:subject_id>/<int:chapter_id>/", course.subject_chapter_update, name="dashboard-subject-chapter-update"),
    path("subject/chapter/delete/<int:subject_id>/<int:chapter_id>/", course.subject_chapter_delete, name="dashboard-subject-chapter-delete"),


    #lesson inside the chapter
    path("chapter/lesson/list/<int:chapter_id>/", course.chapter_lesson_list, name="dashboard-chapters-lesson-list"), #here list the lesson
    path("chapter/lesson/detail/<int:pk>/", course.chapter_detail_lesson, name="dashboard-chapters-lesson-detail"),
    path("chapter/lesson/add/<int:pk>/", course.chapter_lesson_add, name="dashboad-chapter-lesson-add"),
    path("chapter/lesson/update/<int:chapter_id>/<int:lesson_id>/", course.chapter_lesson_update, name="dashboard-chapter-lesson-update"),
    path("chapter/lesson/delete/<int:chapter_id>/<int:lesson_id>/", course.chapter_lesson_delete, name="dashboard-chapter-lesson-delete"),
    # ==================================== Course ============================================= #

    path("subject/", subject.manager, name="dashboard-subject"),
    path("subject/add/", subject.add, name="dashboard-subject-add"),
    path("subject/update/<int:pk>/", subject.update, name="dashboard-subject-update"),
    path("subject/delete/<int:pk>/", subject.delete, name="dashboard-subject-delete"),
]
