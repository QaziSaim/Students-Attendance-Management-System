from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from AMS.models import Course,Session_Year, CustomeUser,Student,Staff,Subject,Staff_Notification,Attendance,Attendance_Report
from django.contrib import messages
from django.http import HttpResponse
import csv
def HOME(request):
    student=Student.objects.filter(admin=request.user.id)
    context={
        'student':student,
    }
    return render(request, 'Student/home.html',context)