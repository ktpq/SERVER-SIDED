from django.shortcuts import render, redirect

from registration.models import *
from django.db.models import Count, Q, F, Value
from django.db.models.functions import Concat
from django.http import HttpResponse

from registration.forms import StudentForm

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
#     faculties =  Faculty.objects.all()
#     sections =  Section.objects.all()
#     return render(request,"create_student.html", context={
#         "faculties": faculties,
#         "sections": sections
#     })

# def create(request):
#     student_id1 = request.POST.get("student_id")
#     faculty1 = request.POST.get("faculty")
#     fn1 = request.POST.get("first_name")
#     ln1 = request.POST.get("last_name")
#     email1 = request.POST.get("email")
#     phone1 = request.POST.get("phone_number")
#     address1 = request.POST.get("address")
#     sections1 = request.POST.getlist("section_ids")

#     fac = Faculty.objects.get(id = faculty1)
#     st1 = Student.objects.create(student_id = student_id1,first_name = fn1,last_name = ln1,faculty=fac)
#     stp1 = StudentProfile.objects.create(student =st1,email = email1,phone_number = phone1,address = address1)

#     for i in sections1:
#           sec = Section.objects.get(id = i)
#           st1.enrolled_sections.add(sec)
#     return redirect("/registration/students")

def create_student(request):
    # faculties =  Faculty.objects.all()
    # sections =  Section.objects.all()

    if request.method == "POST":  
        form = StudentForm(request.POST)
        if form.is_valid():
            # valid
            cd = form.cleaned_data

            newStudent = Student.objects.create(
                student_id = cd["student_id"],
                first_name = cd["first_name"],
                last_name = cd["last_name"],
                faculty = cd["faculty"]
            )

            newProfile = StudentProfile.objects.create(
                student = newStudent,
                email = cd["email"],
                phone_number = cd["phone_number"],
                address = cd["address"]
            )

            newStudent.enrolled_sections.set(cd["enrolled_sections"])
            newStudent.save()
            
            return redirect("student_list")
    else:
        form = StudentForm()
    return render(request, "create_student.html", context={
        "form": form
    })


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