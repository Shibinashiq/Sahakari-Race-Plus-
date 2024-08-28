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
    path("course/detail/<int:pk>/", course.course_detail_subject, name="dashboard-course-detail"), #this endpoint fetch the subjects inside the course
    


    path("course/subject/add/<int:pk>/", course.course_subject_add, name="dashboard-course-subject-add"),
    path("course/subject/update/<int:pk>/", course.course_subject_update, name="dashboard-course-subject-update"),
    path("course/subject/delete/<int:pk>/", course.course_subject_delete, name="dashboard-course-subject-delete"),

    # ==================================== Course ============================================= #

    path("subject/", subject.manager, name="dashboard-subject"),
    path("subject/add/", subject.add, name="dashboard-subject-add"),
    path("subject/update/<int:pk>/", subject.update, name="dashboard-subject-update"),
    path("subject/delete/<int:pk>/", subject.delete, name="dashboard-subject-delete"),
]
