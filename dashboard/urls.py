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
  talenthunt,
  level,
  talenthuntsubject,
  schedule,
  staff,
  comment,
  banner,
  # success_stories,
  folder,
  batchlesson
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


    path("batch/schedule/manager/<int:pk>/", batch.schedule, name="dashboard-batch-schedule-manager"),
    path('merge-lessons/', batch.merge, name='dashboard-lesson-merge-manager'),

    path("batch/subscription/<int:pk>/", batch.subscription_view, name="dashboard-batch-subscripton-manager"),
    path("batch/subscription/list/<int:pk>/", batch.subscription, name="dashboard-batch-subscripton-list"),
    # path("batch/subscription/list/<int:pk>/", batch.customer_add, name="dashboard-batch-subscripton-add"),
    path("batch/batch/subscription/add/<int:batch_id>/", batch.add_customer, name="dashboard-batch-subscripton-add"),
    path("batch/subscription/update/<int:batch_id>/<int:customer_id>/", batch.update_customer, name="dashboard-batch-subscripton-update"),
    path("batch/subscription/delete/<int:customer_id>/<int:batch_id>/", batch.delete_customer, name="dashboard-batch-subscripton-delete"),



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

    path("chapter/question/update/<int:question_id>/<int:chapter_id>/", course.chapter_question_update, name="dashboard-chapter-question-update"),
    path("chapter/question/delete/<int:question_id>/<int:chapter_id>/", course.chapter_question_delete, name="dashboard-chapter-question-delete"),
    path("chapter/question/import/<int:chapter_id>/", course.upload_question_file, name="dashboard-chapter-question-import"),



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
    

    # ==================================== Folder Management ============================================= #

    path("folder/<int:folder_id>/", folder.manager, name="dashboard-folder"),
    path("folder/add/", folder.add, name="dashboard-folder-add"),

    path("folder/update/", folder.update, name="dashboard-folder-update"),
    path("folder/delete/", folder.delete, name="dashboard-folder-delete"),
    path("folder/lesson/add/<int:pk>/", folder.lesson_add, name="dashboard-folder-lesson-add"),
    path("folder/lesson/update/<int:pk>/<int:folder_id>/", folder.lesson_update, name="dashboard-folder-lesson-update"),
    path("folder/lesson/delete/<int:folder_id>/<int:lesson_id>/", folder.lesson_delete, name="dashboard-folder-lesson-delete"),

    # ==================================== Lesson Management ============================================= #

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
    path("customer/exam/result/<int:pk>/", customer.result, name="dashboard-customer-exam-result"),


    path("subscription/customer/update/<int:pk>/", customer.subscription_customer_update, name="dashboard-subscription-customer-update"),
    path("customer/subscription/add/<int:pk>/", customer.subscription_add, name="dashboard-customer-subscription-add"),
    path("customer/subscription/delete/<int:pk>/", customer.subscription_delete, name="dashboard-customer-subscription-delete"),

    # ==================================== Exam Management ============================================= #
   
    path("exam/", exam.manager, name="dashboard-exam-manager"),
    path("exam/list", exam.list, name="dashboard-exam-list"),
    path("exam/add", exam.add, name="dashboard-exam-add"),
    path("exam/update/<int:pk>/", exam.update, name="dashboard-exam-update"),
    path("exam/delete/<int:pk>/", exam.delete, name="dashboard-exam-delete"),
    path("exam/paste/", exam.paste, name="dashboard-exam-paste"),
    path("exam/question/import/<int:exam_id>/", exam.upload_question_file, name="dashboard-exam-question-import"),
  

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


    # ==================================== Talent Hunt Management ============================================= #
   
    path("talenthunt/", talenthunt.manager, name="dashboard-talenthunt-manager"),
    path("talenthunt/list/", talenthunt.list, name="dashboard-talenthunt-list"),
    path("talenthunt/add/", talenthunt.add, name="dashboard-talenthunt-add"),
    path("talenthunt/update/<int:pk>/", talenthunt.update, name="dashboard-talenthunt-update"),
    path("talenthunt/delete/<int:pk>/", talenthunt.delete, name="dashboard-talenthunt-delete"),


    path('fetch-course-subjects/', talenthunt.fetch_course_subjects, name='fetch-course-subjects'),


    path("talenthunt/subject/manager/<int:pk>/", talenthuntsubject.manager, name="dashboard-talenthunt-subject-manager"),
    path("talenthunt/subject/list/<int:pk>/", talenthuntsubject.list, name="dashboard-talenthunt-subject-list"),
    path("talenthunt/subject/add/<int:pk>/", talenthuntsubject.add, name="dashboard-talenthunt-subject-add"),
    path("talenthunt/subject/update/<int:pk>/", talenthuntsubject.update, name="dashboard-talenthunt-subject-update"),
    path("talenthunt/subject/delete/<int:pk>/", talenthuntsubject.delete, name="dashboard-talenthunt-subject-delete"),



    path("level/<int:pk>/", level.manager, name="dashboard-level-manager"),
    path("level/list/<int:pk>/", level.list, name="dashboard-level-list"),
    path("level/add/<int:pk>/", level.add, name="dashboard-level-add"),
    path("level/update/<int:pk>/<int:level_id>/", level.update, name="dashboard-level-update"),
    path("level/delete/<int:pk>/", level.delete, name="dashboard-level-delete"),


    path("level/paste/", level.paste, name="dashboard-level-paste"),
    path("level/question/<int:pk>/", level.level_question_manager, name="dashboard-level-question-manager"),
    path("level/question/list/<int:pk>/", level.level_question_list, name="dashboard-level-question-list"),
    path("level/question/add/<int:pk>/", level.level_question_add, name="dashboard-level-question-add"),
    path("level/question/update/<int:pk>/", level.level_question_update, name="dashboard-level-question-update"),
    path("level/question/delete/<int:pk>/", level.level_question_delete, name="dashboard-level-question-delete"),
    path("level/question/import/<int:exam_id>/", level.upload_question_file, name="dashboard-level-question-import"),


   # ==================================== Schedule Management ============================================= #


    path("schedule/", schedule.manager, name="dashboard-schedule-manager"),
    path("schedule/list", schedule.list, name="dashboard-schedule-list"),
    path("schedule/add/", schedule.add, name="dashboard-schedule-add"),
    path("schedule/update/<int:pk>/", schedule.update, name="dashboard-schedule-update"),
    path("schedule/delete/<int:pk>/", schedule.delete, name="dashboard-schedule-delete"),


  # ==================================== Staff Management ============================================= #
    path("staff/", staff.manager, name="dashboard-staff-manager"),
    path("staff/list/", staff.list, name="dashboard-staff-list"),
    path("staff/add/", staff.add, name="dashboard-staff-add"),
    path("staff/update/<int:pk>/", staff.update, name="dashboard-staff-update"),
    path("staff/disable/<int:pk>/", staff.disable, name="dashboard-staff-disable"),
    path("staff/password/<int:pk>/", staff.set_password, name="dashboard-staff-password-set"),

   # ==================================== Comment Management ============================================= #
    path("comment/", comment.manager, name="dashboard-comment-manager"),
    path("comment/list/", comment.list, name="dashboard-comment-list"),
    path("comment/delete/<int:pk>/", comment.delete, name="dashboard-comment-delete"),
   # ==================================== Staff Management ============================================= #
    path("banner/", banner.manager, name="dashboard-banner-manager"),
    path("banner/list/", banner.list, name="dashboard-banner-list"),
    path("banner/add/", banner.add, name="dashboard-banner-add"),
    path("banner/update/<int:pk>/", banner.update, name="dashboard-banner-update"),
    path("banner/delete/<int:pk>/", banner.delete, name="dashboard-banner-delete"),

   # ==================================== Staff Management ============================================= #
    # path("success-stories/", success_stories.manager, name="dashboard-success-stories-manager"),
    # path("success-stories/list/", success_stories.list, name="dashboard-success-stories-list"),
    # path("success-stories/add/", success_stories.add, name="dashboard-success-stories-add"),
    # path("success-stories/update/<int:pk>/", success_stories.update, name="dashboard-success-stories-update"),
    # path("success-stories/delete/<int:pk>/", success_stories.delete, name="dashboard-success-stories-delete"),

  # ==================================== Staff Management ============================================= #
  
    path("batch-lesson/delete/<int:pk>/", batchlesson.batchlesson_delete, name="dashboard-batch-lesson-delete"),
    path("batch-lesson/update/<int:pk>/", batchlesson.batchlesson_update, name="dashboard-batch-lesson-update"),



]
