from django.urls import path

from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name='index'),
    path("student/create/", views.CreateStudentView.as_view(), name='create_student'),
    path("student/update/<str:student_id>", views.UpdateStudentView.as_view(), name='update_student'),
    path("professor/", views.ProfessorView.as_view(), name='professor'),
    path("course/", views.CourseView.as_view(), name='course'),
    path("course/create/", views.CreateCourseView.as_view(), name='create_course'),
    path("course/update/<str:course_code>", views.UpdateCourseView.as_view(), name='update_course'),
    path("faculty/", views.FacultyView.as_view(), name='faculty'),
    path("nav/", views.NavigationView.as_view(), name='nav'),
]