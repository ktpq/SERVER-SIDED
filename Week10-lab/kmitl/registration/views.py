from django.shortcuts import render, redirect

from registration.models import *
from django.db.models import Count, Q, F, Value
from django.db.models.functions import Concat
from django.http import HttpResponse
from django.views import View
from registration.forms import StudentForm, StudentProfileForm, CourseForm, SectionForm

# Create your views here.
def student_list(request):
    search = request.GET.get("search", "").strip()
    filter_type = request.GET.get("filter", "")
    student_list = Student.objects.all()

    if search:
        if filter_type == "email":
            student_list = Student.objects.filter(studentprofile__email__icontains = search)
        elif filter_type == "faculty":
            student_list = Student.objects.filter(faculty__name__icontains = search)
        else:
            student_list = Student.objects.annotate(
                full_name = Concat('first_name', Value(' '), 'last_name')
            ).filter(
                Q(full_name__icontains = search) | Q(first_name__icontains=search) | Q(last_name__icontains=search)
            )
    return render(request, 'index.html', context={
        'search': search,
        'filter': filter_type,
        'student_list': student_list,
        'total': student_list.count()
    })

def professor_list(request):
    search = request.GET.get("search", "").strip()
    filter_type = request.GET.get("filter", "")
    professor_list = Professor.objects.all()

    if search:
        if filter_type == "faculty":
            professor_list = Professor.objects.filter(faculty__name__icontains=search)
        else:
            professor_list = Professor.objects.annotate(
                full_name=Concat('first_name', Value(' '), 'last_name')
            ).filter(
                Q(full_name__icontains=search) | Q(first_name__icontains=search) | Q(last_name__icontains=search)
            )

    return render(request, 'professor.html', context={
        'total': professor_list.count(),
        'professor_list': professor_list,
        'search': search,
        'filter': filter_type
    })


def faculty_list(request):
    search = request.GET.get("search", "").strip()
    faculty_list = Faculty.objects.annotate(professor_count = Count("professor", distinct=True), student_count = Count("student", distinct=True)).all()
    
    if search:
        faculty_list = Faculty.objects.annotate(professor_count = Count("professor", distinct=True), student_count = Count("student", distinct=True)).filter(name__icontains = search).all()
    return render(request, "faculty.html", context={
        "faculty_list": faculty_list,
        "total": faculty_list.count(),
        "search": search
    })

def course_list(request):
    search = request.GET.get("search", "").strip()
    course_list = Course.objects.all()
    
    if search:
        course_list = Course.objects.filter(course_name__icontains = search).all()
    return render(request, "course.html", context={
        "course_list": course_list,
        "total": course_list.count(),
        "search": search
    })



# def create_student(request):
#     # faculties =  Faculty.objects.all()
#     # sections =  Section.objects.all()

#     if request.method == "POST":  
#         form = StudentForm(request.POST)
#         if form.is_valid():
#             # valid
#             cd = form.cleaned_data

#             newStudent = Student.objects.create(
#                 student_id = cd["student_id"],
#                 first_name = cd["first_name"],
#                 last_name = cd["last_name"],
#                 faculty = cd["faculty"]
#             )

#             newProfile = StudentProfile.objects.create(
#                 student = newStudent,
#                 email = cd["email"],
#                 phone_number = cd["phone_number"],
#                 address = cd["address"]
#             )

#             newStudent.enrolled_sections.set(cd["enrolled_sections"])
#             newStudent.save()
            
#             return redirect("student_list")
#     else:
#         form = StudentForm()
#     return render(request, "create_student.html", context={
#         "form": form
#     })

def create_student(request):
    if request.method == "POST":
        stdform = StudentForm(request.POST)
        proform = StudentProfileForm(request.POST)
        if stdform.is_valid() and proform.is_valid():
            student = stdform.save()
            profile = proform.save(commit = False)
            profile.student = student
            profile.save()
            return redirect('student_list')
        
    else:
        # method GET
        stdform = StudentForm()
        proform = StudentProfileForm()
    return render(request, "create_student.html", {"stdform": stdform, "proform": proform}) 

def create_course(request):
    if request.method == "POST":
        c_form = CourseForm(request.POST)
        s_form = SectionForm(request.POST)
        if c_form.is_valid() and s_form.is_valid():
            course = c_form.save()
            section = s_form.save(commit=False)
            section.course = course
            section.save()
            return redirect('course_list')
    else:
        # method get
        c_form = CourseForm()
        s_form = SectionForm()
    return render(request, "create_course.html", { "cform": c_form, "sform": s_form })

def update_course(request, course_code):
    crs = Course.objects.get(course_code = course_code)
    sec = Section.objects.filter(course = crs).first()
    
    if request.method == "POST":
        course_form = CourseForm(request.POST, instance=crs)
        section_form = SectionForm(request.POST, instance=sec)
        if course_form.is_valid() and section_form.is_valid():
            course = course_form.save()
            section = section_form.save(commit=False)
            section.course = course
            section.save()
            return redirect('course_list')
        else:
            print(course_form.errors)
            print(section_form.errors)
    else:
        course_form = CourseForm(instance=crs)
        section_form = SectionForm(instance=sec)
    return render(request, "update_course.html", {
        "cform": course_form,
        "sform": section_form,
        "course": crs
    })
    # else:
        # method get
        
        # print(course_code)
        # course = Course.objects.get(course_code = course_code)
        # section = Section.objects.filter(course = course).first()
        # c_form = CourseForm(request.POST, )
        # s_form = SectionForm()
        
    # return render(request, "create_course.html", { "cform": c_form, "sform": s_form })

# course = Course.objects.get(course_code = course_code)
#     section = Section.objects.filter(course = course).first()

#     if request.method == "POST":
#         course_form = CourseForm(request.POST, instance=course)
#         section_form = SectionForm(request.POST, instance=section)

#         if course_form.is_valid() and section_form.is_valid():
#             c_form = course_form.save()
#             s_form = section_form.save(commit=False)
#             s_form.course = 


def update_student(request, student_id):
    student = Student.objects.get(student_id = student_id)
    pro = StudentProfile.objects.get(student = student)
    data = {
        "student_id": student.student_id,
        "first_name": student.first_name,
        "last_name": student.last_name,
        "faculty": student.faculty,
        "email": pro.email,
        "phone_number": pro.phone_number,
        "address": pro.address,
        "enrolled_sections": student.enrolled_sections.all()
    }
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            student.student_id = cd["student_id"]
            student.first_name = cd["first_name"]
            student.last_name = cd["last_name"]
            student.faculty = cd["faculty"]
            student.save()
            pro.email = cd["email"]
            pro.phone_number = cd["phone_number"]
            pro.address = cd["address"]
            pro.save()

            student.enrolled_sections.set(cd["enrolled_sections"])
            return redirect("student_list")
    else:
        form = StudentForm(initial=data)
    return render(request, "update_student.html", {"form": form, "student_id": student_id})