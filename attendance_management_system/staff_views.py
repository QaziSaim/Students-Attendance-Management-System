from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from AMS.models import Course,Session_Year, CustomeUser,Student,Staff,Subject,Staff_Notification,Attendance,Attendance_Report,LeaveReportStaff,LeaveReportStudent
from django.contrib import messages
from django.http import HttpResponse
import csv
from django.core.mail import send_mail
from django.db.models import Count, Sum,Case,When
from AMS.forms import TakeAttendance
from django.db import models

from django.conf import settings
from twilio.rest import Client
from datetime import datetime

# 

# 
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.forms import formset_factory
from .send_sms import SEND_SMS
# @login_required(login_url='/')
@login_required(login_url='/')
def HOME(request):
    staff=Staff.objects.filter(admin=request.user.id)
    staff_id=Staff.objects.get(admin=request.user.id)
    subject=Subject.objects.filter(staff=staff_id)
    context={
        'staff':staff,
        'subject':subject,
    }
    return render(request, 'Staff/home.html',context)
@login_required(login_url='/')
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
@login_required(login_url='/')
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
                subject=get_subject,
            )
            attendance_report.save()
            messages.success(request, "The Attendance have been taking successfully")
    
            # print(student_id)
    return redirect('staff_take_attendance')
@login_required(login_url='/')
def STAFF_VIEW_ATTENDANCE(request):
    staff_id = Staff.objects.get(admin=request.user.id)
    # Retrieve all subjects taught by the current staff member
    subjects = Subject.objects.filter(staff_id=staff_id)

    # Handle form submission
    if request.method == "POST":
        # Retrieve the form data
        subject_id = request.POST.get("subject_id")
        attendance_date = request.POST.get("attendance_date")
        # Retrieve the subject and attendance records for the selected date
        subject = Subject.objects.get(id=subject_id)
        attendance_records = Attendance.objects.filter(
            subject_id=subject, attendance_date=attendance_date
        )
        # Create a dictionary to store attendance data for each student
        student_attendance = {}
        for record in attendance_records:
            for student in record.student_id.all():
                student_attendance.setdefault(student, []).append(record.mark)

        context = {
            "subjects": subjects,
            "subject": subject,
            "attendance_records": attendance_records,
            "attendance_date": attendance_date,
            "student_attendance": student_attendance,
        }
        return render(request, "Staff/staff_view_attendance.html", context)

    context = {"subjects": subjects}
    return render(request, "Staff/staff_view_attendance.html", context)
    # staff_id=Staff.objects.get(admin=request.user.id)
    # subject=Subject.objects.filter(staff_id=staff_id)
    # action=request.GET.get('action')
    # get_subject=None
    # attendance_report=None
    # attendance_date=None
    # if action is not None:
    #     if request.method=="POST":
    #         subject_id=request.POST.get('subject_id')
    #         attendance_date=request.POST.get('attendance_date')
    #         get_subject=Subject.objects.get(id=subject_id)
    #         attendace=Attendance.objects.filter(subject_id=get_subject,attendance_date=attendance_date)
    #         for i in attendace:
    #             attendance_id=i.id
    #             attendance_report=Attendance.objects.filter(attendance_id=attendance_id)

  
    # context={
    #     'subject':subject,
    #     'action':action,
    #     'get_subject':get_subject,
    #     'attendance_date':attendance_date,
    #     'attendance_report':attendance_report,

    # }
    # return render(request, 'Staff/view_attendance.html',context)

@login_required(login_url='/')
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
@login_required(login_url='/')
def NOTIFICATION(request):
    staff=Staff.objects.filter(admin=request.user.id)
    for i in staff:
        staff_id=i.id
        notification=Staff_Notification.objects.filter(staff_id=staff_id)
        context={
        'notification':notification
        }
    return render(request, 'Staff/notification.html',context)
@login_required(login_url='/')
def DELET_NOTIFICATION(request):
    notification=Staff_Notification.objects.get(id=id)
    notification.delete()
    return redirect('notifications')
def STAFF_APPLY_LEAVE(request):
    return render(request, "Staff/apply_leave.html")
def sendMsg(date, absentees, no_of_absentees):
    absentees_phone = []
    absentees_name = []
    absentees_sem = []
    attendance_percent = []
    for x in absentees:
        data = Student.objects.filter(usn=x)[0]
        absentees_attendance = Attendance.objects.filter(usn=x)[0]
        attendance_percent.append(str(absentees_attendance.percent))
        absentees_phone.append(str(data.parent_phone))
        absentees_name.append(str(data.name))
        absentees_sem.append(str(data.sem))

    for z in range(no_of_absentees):
        mobile_no = str(absentees_phone[z])
        message = "You ward %s studying in Semester %s has not attended the classes on %s and is currently having " \
                  "the attendance percentage of %s.\n-Dr. Manjunath R\n HOD, Dept of CSE\n RRIT\n" % \
                  (absentees_name[z], absentees_sem[z], date, attendance_percent[z])
        sendPostRequest(URL, 'your key', 'your key', 'stage', mobile_no, 'identifier', message)
def take_attendance(request):
    staff_id=Staff.objects.get(admin=request.user.id)
    subjects=Subject.objects.filter(staff=staff_id)
    students=None
    for i in subjects:
        student__id=i.course
        students=Student.objects.filter(course_id=student__id)
    if request.method == 'POST':
        fm = TakeAttendance(request.POST)
        if fm.is_valid():
            st=fm.cleaned_data['student_id']
            su=fm.cleaned_data['subject_id']
            dt=fm.cleaned_data['attendance_date']
            mk=fm.cleaned_data['mark']
            # if Attendance.objects.filter(student_id=st).exists():
            #     messages.warning(request, 'Attendance is already taken for this student on this date.')
            #     return redirect('attendance')
            # elif Attendance.objects.filter(attendance_date=dt).exists():
            #     messages.warning(request, 'Attendance is already taken for this student on this date.')
            #     return redirect('attendance')
            # else:
            #     take = Attendance(student_id=st, subject_id=su, attendance_date=dt, mark=mk)
            #     take.save()
            #     return redirect('attendance')

            take=Attendance(subject_id=su,attendance_date=dt,mark=mk)
            take.save()
            take.student_id.set(st)
            SEND_SMS()
            messages.success(request, "The Attendance have been taking successfully")
            return redirect('attendance')
    else:
        fm=TakeAttendance()
    fm.fields['subject_id'].queryset=subjects
    fm.fields['student_id'].queryset=students
    return render(request, 'Staff/attendance.html',{'form':fm})

def send_sms(request, date):
    # get the absent students for the given date
    absent_students = Attendance.objects.filter(
        attendance_date=date,
        mark=1
    ).distinct()
    
    # create the SMS message body
    message_body = f"Dear student, you were marked absent on {date}. Please contact your teacher for more information."
    
    # send an SMS message to each absent student
    for student in absent_students:
        phone_number = student.phone_number
        
        # send the SMS message using the Twilio client
        twilio_client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        twilio_client.messages.create(
            to=phone_number,
            from_=settings.TWILIO_FROM_NUMBER,
            body=message_body
        )
    
    return render(request, 'sms_sent.html')

def PRESENT_REPORT(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Student_Details.csv'

    # Create a csv writer
    writer = csv.writer(response)

    # Get the attendance records grouped by student and subject and calculate the total present days for each subject
    attendance_query = Attendance.objects.values('student_id').annotate(
        **{
            subject.name: Sum(Case(When(subject_id=subject.id, mark='1', then=1), output_field=models.IntegerField()))
            for subject in Subject.objects.all()
        },
        total_present=Sum(Case(When(mark='1', then=1), output_field=models.IntegerField())),
        total_absent=Sum(Case(When(mark='0', then=1), output_field=models.IntegerField())),
        total_days=Count('id'),
    )

    # Add column headers
    writer.writerow(['Student ID', 'Student Name'] + list(Subject.objects.values_list('name', flat=True)) + ['Total Present Days', 'Total Absent Days', 'Percentage'])

    # Loop through and output
    for attendance in attendance_query:
        student = Student.objects.get(id=attendance['student_id'])
        total_present = attendance['total_present']
        total_absent = attendance['total_absent']
        total_days = attendance['total_days']
        percentage = round((total_present / total_days) * 100, 2)
        
        # Write row data
        writer.writerow([student.id, student.admin] + [attendance[subject.name] for subject in Subject.objects.all()] + [total_present, total_absent, f"{percentage}%"])

    return response


def staff_apply_leave(request):
    staff_obj = Staff.objects.get(admin=request.user.id)
    leave_data = LeaveReportStaff.objects.filter(staff_id=staff_obj)
    context = {
        "leave_data": leave_data
    }
    return render(request, "Staff/staff_apply_leave_template.html", context)


def staff_apply_leave_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('staff_apply_leave')
    else:
        leave_date = request.POST.get('leave_date')
        leave_message = request.POST.get('leave_message')

        staff_obj = Staff.objects.get(admin=request.user.id)
        try:
            leave_report = LeaveReportStaff(staff_id=staff_obj, leave_date=leave_date, leave_message=leave_message, leave_status=0)
            leave_report.save()
            messages.success(request, "Applied for Leave.")
            return redirect('staff_apply_leave')
        except:
            messages.error(request, "Failed to Apply Leave")
            return redirect('staff_apply_leave')

