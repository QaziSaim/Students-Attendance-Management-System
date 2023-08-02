from django.shortcuts import render,redirect
from AMS.models import *
from django.contrib import messages
from django.http import HttpResponse
def HOME(request):
    student=Student.objects.filter(admin=request.user.id)
    # course=Course.objects.all()
    student_id=Student.objects.get(admin=request.user.id)

    # course=Course.objects.filter(name=student_id)
    # course=Course.objects.filter(staff=staff_id)
    context={
        'student':student,
        # 'subject':subject,
        # 'course':course
    }
    return render(request, 'Student/home.html',context)


def student_apply_leave(request):
    student_obj = Student.objects.get(admin=request.user.id)
    leave_data = LeaveReportStudent.objects.filter(student_id=student_obj)
    context = {
        "leave_data": leave_data
    }
    return render(request, 'Student/student_apply_leave.html', context)


def student_apply_leave_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('student_apply_leave')
    else:
        leave_date = request.POST.get('leave_date')
        leave_message = request.POST.get('leave_message')

        student_obj = Student.objects.get(admin=request.user.id)
        try:
            leave_report = LeaveReportStudent(student_id=student_obj, leave_date=leave_date, leave_message=leave_message, leave_status=0)
            leave_report.save()
            messages.success(request, "Applied for Leave.")
            return redirect('student_apply_leave')
        except:
            messages.error(request, "Failed to Apply Leave")
            return redirect('student_apply_leave')

