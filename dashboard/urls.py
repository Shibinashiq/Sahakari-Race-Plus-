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
    customer,
    batch,
    chapter,
    lesson,
    exam,
    question,
   
)

urlpatterns = [
    # ==================================== Authentication ============================================= #

    path("login/", authentication.login, name="dashboard-login"),
    path("logout/", auth_views.LogoutView.as_view(), name="dashboard-logout"),

    # ==================================== Home ============================================= #
    
    path("", home.home, name="dashboard-home"),



    # ==================================== Batch ============================================= #
    path("batch/", batch.manager, name="dashboard-batch"),
    path("batch/list", batch.list, name="dashboard-batch-list"),
    path("batch/add/", batch.add, name="dashboard-batch-add"),
    path("batch/update/<int:pk>/", batch.update, name="dashboard-batch-update"),
    path("batch/delete/<int:pk>/", batch.delete, name="dashboard-batch-delete"),



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


    #question inside the lesson
    path("chapter/question/list/<int:chapter_id>/", course.chapter_question_list, name="dashboard-chapter-question-list"), #here list the question
    path("chapter/question/detail/<int:pk>/", course.chapter_detail_question, name="dashboard-chapter-question-detail"),
    path("chapter/question/add/<int:pk>/", course.chapter_question_add, name="dashboard-chapter-question-add"),  

    path("chapter/question/update/<int:chapter_id>/<int:question_id>/", course.chapter_question_update, name="dashboard-chapter-question-update"),
    path("chapter/question/delete/<int:chapter_id>/<int:question_id>/", course.chapter_question_delete, name="dashboard-chapter-question-delete"),
    # ==================================== Subject Management ============================================= #

    path("subject/", subject.manager, name="dashboard-subject"),
    path("subject/list", subject.list, name="dashboard-subject-list"),
    path("subject/add/", subject.add, name="dashboard-subject-add"),
    path("subject/update/<int:pk>/", subject.update, name="dashboard-subject-update"),
    path("subject/delete/<int:pk>/", subject.delete, name="dashboard-subject-delete"),

    # ==================================== Chapter Management ============================================= #

    path("chapter/", chapter.manager, name="dashboard-chapter"),
    path("chapter/list", chapter.list, name="dashboard-chapter-list"),
    path("chapter/add/", chapter.add, name="dashboard-chapter-add"),
    path("chapter/update/<int:pk>/", chapter.update, name="dashboard-chapter-update"),
    path("chapter/delete/<int:pk>/", chapter.delete, name="dashboard-chapter-delete"),
    # ==================================== Chapter Management ============================================= #

    path("lesson/", lesson.manager, name="dashboard-lesson"),
    path("lesson/list", lesson.list, name="dashboard-lesson-list"),
    path("lesson/add/", lesson.add, name="dashboard-lesson-add"),
    path("lesson/update/<int:pk>/", lesson.update, name="dashboard-lesson-update"),
    path("lesson/delete/<int:pk>/", lesson.delete, name="dashboard-lesson-delete"),

    # ==================================== Customer Management ============================================= #

    path("customer/", customer.manager, name="dashboard-customer"),
    path("customer/list", customer.list, name="dashboard-customer-list"),
    path("customer/add", customer.add, name="dashboard-customer-add"),
    path("customer/update/<int:pk>/", customer.update, name="dashboard-customer-update"),
    path("customer/delete/<int:pk>/", customer.delete, name="dashboard-customer-delete"),
    path("customer/detail/<int:pk>/", customer.detail, name="dashboard-user-detail"),

    # ==================================== Exam Management ============================================= #
   
    path("exam/", exam.manager, name="dashboard-exam-manager"),
    path("exam/list", exam.list, name="dashboard-exam-list"),
    path("exam/add", exam.add, name="dashboard-exam-add"),
    path("exam/update/<int:pk>/", exam.update, name="dashboard-exam-update"),
    path("exam/delete/<int:pk>/", exam.delete, name="dashboard-exam-delete"),


    path("exam/question/<int:exam_id>/", exam.exam_question_manager, name="dashboard-exam-question-manager"),
    path("exam/question/list/<int:exam_id>/", exam.exam_question_list, name="dashboard-exam-question-list"),
    path("exam/question/add/<int:exam_id>/", exam.exam_question_add, name="dashboard-exam-question-add"),
    path("exam/question/update/<int:exam_id>/<int:question_id>/", exam.exam_question_update, name="dashboard-exam-question-update"),
    path("exam/question/delete/<int:exam_id>/<int:question_id>/", exam.exam_question_delete, name="dashboard-exam-question-delete"),
    

   # ==================================== Question Management ============================================= #

    path("question/", question.manager, name="dashboard-question-manager"),
    path("question/list", question.list, name="dashboard-question-list"),
    path("question/add", question.add, name="dashboard-question-add"),
    path("question/update/<int:pk>/", question.update, name="dashboard-question-update"),
    path("question/delete/<int:pk>/", question.delete, name="dashboard-question-delete"),




    
]
