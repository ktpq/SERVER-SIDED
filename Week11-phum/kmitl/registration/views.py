from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View

from registration.models import *
from registration.forms import *

from django.db.models.functions import Concat
from django.db.models import Value
from django.db.models.query import QuerySet

from django.db import transaction


def search_handler(request, query_list: QuerySet, map_filter):
    search = request.GET.get('search', '')
    sfilter = request.GET.get('filter', '')
    return {
        'query_list': query_list.filter(**{map_filter[sfilter]:search}),
        'filter' : sfilter
    }

# Create your views here.
class IndexView(View):
    def get(self, request):
        map_filter = {
            '' : 'full_name__icontains',
            'email' : 'studentprofile__email__icontains',
            'faculty' : 'faculty__name__icontains',
            }
        query_list = (
            Student.objects
            .annotate(full_name=Concat('first_name', Value(' '), 'last_name'))
            .order_by('student_id')
            )
        sresult = search_handler(request, query_list, map_filter)
        context = {
            'total' : sresult['query_list'].count(),
            'student_list' : sresult['query_list'],
            'filter' : sresult['filter']
        }
        return render(request, 'index.html', context)

class ProfessorView(View):
    def get(self, request):
        map_filter = {
            '' : 'full_name__icontains',
            'faculty' : 'faculty__name__icontains'
            }
        query_list = (
            Professor.objects
            .annotate(full_name=Concat('first_name', Value(' '), 'last_name'))
            )
        sresult = search_handler(request, query_list, map_filter)
        context = {
            'total' : sresult['query_list'].count(),
            'professor_list' : sresult['query_list'],
            'filter' : sresult['filter']
        }
        return render(request, 'professor.html', context)

class CourseView(View):
    def get(self, request):
        map_filter = {'' : 'course_name__icontains'}
        query_list = Course.objects.all()
        sresult = search_handler(request, query_list, map_filter)
        context = {
            'total' : sresult['query_list'].count(),
            'course_list' : sresult['query_list'],
            'filter' : sresult['filter']
        }
        return render(request, 'course.html', context)

class FacultyView(View):
    def get(self, request):
        map_filter = {'' : 'name__icontains'}
        query_list = Faculty.objects.all()
        sresult = search_handler(request, query_list, map_filter)
        context = {
            'total' : sresult['query_list'].count(),
            'faculty_list' : sresult['query_list'],
            'filter' : sresult['filter']
        }
        return render(request, 'faculty.html', context)

class NavigationView(View):
    def get(self, request):
        return render(request, 'nav.html')

class CreateStudentView(View):
    def get(self, request):
        studentForm = StudentForm()
        studentProfileForm = StudentProfileForm()
        context = {
            "studentForm": studentForm, 
            "studentProfileForm": studentProfileForm, 
        }
        return render(request, 'create_student.html', context)

    def post(self, request):
        studentForm = StudentForm(request.POST)
        studentProfileForm = StudentProfileForm(request.POST, request.FILES)
        
        try:
            with transaction.atomic():
                if studentForm.is_valid():
                    student = studentForm.save()
                    if studentProfileForm.is_valid():
                        profile = studentProfileForm.save(commit=False)
                        profile.student = student
                        profile.save()
                        return redirect('index')
                    else:
                        raise transaction.TransactionManagementError("Invalid StudentProfileForm")
                else:
                    raise transaction.TransactionManagementError("Invalid StudentForm")
        except Exception:
            context = {
                "studentForm": studentForm, 
                "studentProfileForm": studentProfileForm, 
            }
            return render(request, 'create_student.html', context)

class UpdateStudentView(View):
    def get(self, request, student_id):
        student = Student.objects.get(student_id=student_id)
        studentForm = StudentForm(instance=student)
        studentProfileForm = StudentProfileForm(instance=student.studentprofile)
        context = {
            "studentForm": studentForm, 
            "studentProfileForm": studentProfileForm, 
        }
        return render(request, 'update_student.html', context)
    
    def post(self, request, student_id):
        student = Student.objects.get(student_id=student_id)
        studentForm = StudentForm(request.POST, instance=student)
        studentProfileForm = StudentProfileForm(request.POST, request.FILES, instance=student.studentprofile)
        try:
            with transaction.atomic():
                if studentForm.is_valid():
                    student = studentForm.save()
                    if studentProfileForm.is_valid():
                        profile = studentProfileForm.save(commit=False)
                        profile.student = student
                        profile.save()
                        return redirect('index')
                    else:
                        raise transaction.TransactionManagementError("Invalid StudentProfileForm")
                else:
                    raise transaction.TransactionManagementError("Invalid StudentForm")
        except Exception:
            context = {
                "studentForm": studentForm, 
                "studentProfileForm": studentProfileForm, 
            }
            return render(request, 'create_student.html', context)
    
class CreateCourseView(View):
    def get(self, request):
        courseForm = CourseForm()
        sectionForm = SectionForm()
        context = {
            "courseForm": courseForm,
            "sectionForm": sectionForm
        }
        return render(request, 'create_course.html', context)

    def post(self, request):
        courseForm = CourseForm(request.POST)
        sectionForm = SectionForm(request.POST)

        if courseForm.is_valid() and sectionForm.is_valid():
            course = courseForm.save()
            section = sectionForm.save(commit=False)
            section.course = course
            section.save()
            return redirect('course')
        context = {
            "courseForm": courseForm,
            "sectionForm": sectionForm
        }
        return render(request, 'create_course.html', context)

class UpdateCourseView(View):
    def get(self, request, course_code):
        course = Course.objects.get(course_code=course_code)
        courseForm = CourseForm(instance=course)
        sectionForm = SectionForm(instance=course.section_set.first())
        sectionFormSet = SectionFormSet(queryset=course.section_set.all())
        context = {
            "courseForm": courseForm,
            "sectionForm": sectionForm,
            "sectionFormSet": sectionFormSet
        }
        return render(request, 'update_course.html', context)

    def post(self, request, course_code):
        course = Course.objects.get(course_code=course_code)
        courseForm = CourseForm(request.POST, instance=course)
        sectionFormSet = SectionFormSet(request.POST, queryset=course.section_set.all())
        if courseForm.is_valid() and sectionFormSet.is_valid():
            course = courseForm.save()
            sections = sectionFormSet.save(commit=False)
            for deleting in sectionFormSet.deleted_objects:
                deleting.delete()
                
            for section in sections:
                section.course = course
                section.save()
            return redirect('course')
        context = {
            "courseForm": courseForm,
            "sectionFormSet": sectionFormSet
        }
        print(courseForm.is_valid(), courseForm.errors)
        print(sectionFormSet.is_valid(), sectionFormSet.errors)
        return render(request, 'update_course.html', context)