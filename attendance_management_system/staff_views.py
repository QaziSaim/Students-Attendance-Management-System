from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from AMS.models import Course,Session_Year, CustomeUser,Student,Staff,Subject,Staff_Notification,Attendance,Attendance_Report
from django.contrib import messages
from django.http import HttpResponse
import csv
# @login_required(login_url='/')

def HOME(request):
    staff=Staff.objects.filter(admin=request.user.id)
    staff_id=Staff.objects.get(admin=request.user.id)
    subject=Subject.objects.filter(staff=staff_id)
    context={
        'staff':staff,
        'subject':subject,
    }
    return render(request, 'Staff/home.html',context)
def STAFF_TAKE_ATTENDANCE(request):
    staff_id=Staff.objects.get(admin=request.user.id)
    subject=Subject.objects.filter(staff=staff_id)
    

    action=request.GET.get('action')
    # Temperory None
    get_subject=None
    students=None
# End Here
    if action is not None:
        if request.method=="POST":
            subject_id=request.POST.get('subject_id')
            get_subject=Subject.objects.get(id=subject_id)
            subject=Subject.objects.filter(id=subject_id)
            for i in subject:
                student_id=i.course.id
                students=Student.objects.filter(course_id=student_id)


    context={
        'subject':subject,
        'get_subject':get_subject,
        'action':action,
        'students':students,
    }
    return render(request, 'Staff/take_attendance.html',context)
def STAFF_SAVE_ATTENDANCE(request):
    if request.method=="POST":
        subject_id=request.POST.get('subject_id')
        attendance_date=request.POST.get('attendance_date')
        student_id=request.POST.getlist('student_id')
        get_subject=Subject.objects.get(id=subject_id)
        attendance=Attendance(
            subject_id=get_subject  ,
            attendance_date=attendance_date,

        )
        attendance.save()
        for i in student_id:
            student_id = i
            int_stud=int(student_id)
            p_student=Student.objects.get(id=int_stud)
            attendance_report=Attendance_Report(
                student_id=p_student,
                attendance_id=attendance,
            )
            attendance_report.save()
            # print(student_id)
    return redirect('staff_take_attendance')
def STAFF_VIEW_ATTENDANCE(request):
    staff_id=Staff.objects.get(admin=request.user.id)
    subject=Subject.objects.filter(staff_id=staff_id)
    action=request.GET.get('action')
    get_subject=None
    attendance_report=None
    attendance_date=None
    if action is not None:
        if request.method=="POST":
            subject_id=request.POST.get('subject_id')
            attendance_date=request.POST.get('attendance_date')
            get_subject=Subject.objects.get(id=subject_id)
            attendace=Attendance.objects.filter(subject_id=get_subject,attendance_date=attendance_date)
            for i in attendace:
                attendance_id=i.id
                attendance_report=Attendance_Report.objects.filter(attendance_id=attendance_id)

  
    context={
        'subject':subject,
        'action':action,
        'get_subject':get_subject,
        'attendance_date':attendance_date,
        'attendance_report':attendance_report,

    }
    return render(request, 'Staff/view_attendance.html',context)
def PRESENT_REPORT(request):
    response=HttpResponse(content_type='text/csv')
    response['Content-Disposition']='attachment; filename=Student_Details.csv'
    # Create a csv writer
    writer=csv.writer(response)
    # Designate the model
    student=Student.objects.all()
    attendance=Attendance.objects.all()
    attendance_report=Attendance_Report.objects.all()

    # add column
    writer.writerow(['Student ID','Student Name','Attendance Date'])
    # Loop Through and output
    
    for i in attendance:
        writer.writerow([i.id,i,i.attendance_date])
    return response
