from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from AMS.models import Course,Session_Year, CustomeUser,Student,Staff,Subject,Staff_Notification,Attendance,Attendance_Report
from django.contrib import messages
from django.http import HttpResponse
import csv
from django.core.mail import send_mail
from django.db.models import Count, Sum
from AMS.forms import TakeAttendance

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
    if request.method == 'POST':
        fm = TakeAttendance(request.POST)
        if fm.is_valid():
            st=fm.cleaned_data['student_id']
            su=fm.cleaned_data['subject_id']
            dt=fm.cleaned_data['attendance_date']
            mk=fm.cleaned_data['mark']
            if Attendance.objects.filter(student_id=st, attendance_date=dt,subject_id=su).exists():
                messages.warning(request, 'Attendance is already taken for this student on this date.')
                return redirect('attendance')
            else:
                take = Attendance(student_id=st, subject_id=su, attendance_date=dt, mark=mk)
                take.save()
                return redirect('attendance')

            take=Attendance(student_id=st,subject_id=su,attendance_date=dt,mark=mk)
            take.save()
            return redirect('attendance')
    else:
        fm=TakeAttendance()
    return render(request, 'Staff/attendance.html',{'form':fm}) 
def PRESENT_REPORT(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Student_Details.csv'

    # Create a csv writer
    writer = csv.writer(response)

    # Get the attendance records grouped by student and subject and calculate the total present and absent days
    attendance_query = Attendance.objects.values('student_id', 'subject_id') \
        .annotate(total_present=Sum('mark'), total_absent=Count('mark') - Sum('mark'), total_days=Count('mark'))

    # Add column headers
    writer.writerow(['Student ID', 'Student Name', 'Subject', 'Total Present Days', 'Total Absent Days', 'Percentage'])

    # Loop through and output
    for attendance in attendance_query:
        student = Student.objects.get(id=attendance['student_id'])
        subject = Subject.objects.get(id=attendance['subject_id'])
        total_present = attendance['total_present']
        total_absent = attendance['total_absent']
        total_days = attendance['total_days']
        percentage = round((total_present / total_days) * 100, 2)
        writer.writerow([student.id, student.admin, subject.name, total_present, total_absent, f"{percentage}%"])

    return response
