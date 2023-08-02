from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from AMS.models import Course,Session_Year, CustomeUser,Student,Staff,Subject,Staff_Notification,LeaveReportStaff,LeaveReportStudent
from django.contrib import messages
from django.http import HttpResponse
@login_required(login_url='/')
def home(request):
    student_count=Student.objects.all().count()
    staff_count=Staff.objects.all().count()
    course_count=Course.objects.all().count()
    subject_count=Subject.objects.all().count()

    student_gender_male=Student.objects.filter(gender='Male').count()
    student_gender_female=Student.objects.filter(gender='Female').count()
    print(student_gender_male)
    print(student_gender_female)
    context={
        'student_count':student_count,
        'staff_count':staff_count,
        'course_count':course_count,
        'subject_count':subject_count,
        'student_gender_male':student_gender_male,
        'student_gender_female':student_gender_female,
    }
    return render(request,'Hod/home.html',context)
@login_required(login_url='/')
def ADD_STUDENT(request):
    course=Course.objects.all()
    session_year=Session_Year.objects.all()
    # st=Student.objects.order_by(id)
    if request.method=="POST":
        profile_pic=request.FILES.get('profile_pic')
        username=request.POST.get('username')
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        gender=request.POST.get('gender')
        email=request.POST.get('email')
        password=request.POST.get('password')
        phonenumber=request.POST.get('phone_number')
        address=request.POST.get('address')
        course_id=request.POST.get('course_id')
        session_year_id=request.POST.get('session_year_id')
        if CustomeUser.objects.filter(email=email).exists():
            messages.warning(request,'Email is already exist')
            return redirect('add_student')
        if CustomeUser.objects.filter(username=username).exists():
            messages.warning(request, 'Username is already exist')
            redirect('add_student')
        else:
            user=CustomeUser(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                profile_pic=profile_pic,
                user_type=3
            )
            user.set_password(password)
            user.save()
            course=Course.objects.get(id=course_id)
            if int(course.limit) <= course.student_set.count():
                messages.warning(request, "The course enrollment limit has been reached")
                return redirect("add_student")  
            session_year=Session_Year.objects.get(id=session_year_id)
            student=Student(
                admin=user,
                address=address,
                session_year_id=session_year,
                course_id=course,
                gender=gender,
                phone_number=phonenumber,
                )
            student.save()
            messages.success(request, user.first_name+" "+user.last_name+" "+"Are Successfully Added")
            return redirect('add_student')

    context={
        'course':course,
        'session_year':session_year,
        # 'st':st
    }
    return render(request, 'Hod/add_student.html',context)

def VIEW_STUDENT(request):
    student = Student.objects.all()
    # print(student)
    context={
        'student':student,
    }
    return render(request, 'Hod/view_student.html',context)
def UPDATE_STUDENT(request):
    if request.method=="POST":
        student_id = request.POST.get('student_id')

        profile_pic=request.FILES.get('profile_pic')
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        gender=request.POST.get('gender')
        email=request.POST.get('email')
        username=request.POST.get('username')
        password=request.POST.get('password')
        phonenumber=request.POST.get('phone_number')
        address=request.POST.get('address')
        course_id=request.POST.get('course_id')
        session_year_id=request.POST.get('session_year_id')
        user=CustomeUser.objects.get(id=student_id)

        user.first_name=first_name
        user.last_name=last_name
        user.email=email
        user.username=username
        if profile_pic != None and profile_pic != "":
            user.profile_pic = profile_pic
        if password != None and password != "":
            user.set_password(password)
        user.save()
        student=Student.objects.get(admin=student_id)
        student.address=address
        student.gender=gender
        student.pn=phonenumber
        
        course=Course.objects.get(id=course_id)
        student.course_id=course

        session_year=Session_Year.objects.get(id=session_year_id)
        student.session_year_id=session_year
        student.save()
        messages.success(request,'records are successfully updated')
        return redirect('view_student')



    return render(request,'Hod/edit_student.html')

def EDIT_STUDENT(request,id):
    student=Student.objects.filter(id=id)
    course=Course.objects.all()
    session_year=Session_Year.objects.all()
    context={
        'student':student,
        'course':course,
        'session_year':session_year
    }
    return render(request,'Hod/edit_student.html',context)
def DELETE_STUDENT(request,admin):
    student=CustomeUser.objects.get(id=admin)
    student.delete()
    messages.success(request,'Record are successfully deleted ! ')
    return redirect('view_student')
# Course
def ADD_COURSE(request):
    if request.method=="POST":
        course_name=request.POST.get('course_name')
        if Course.objects.filter(name=course_name).exists():
            messages.warning(request, "Course is already exist")
            return redirect("add_course")
        # user=request.user
        if Course.objects.count()>4:
            messages.warning(request, "The Course Entry is full")
            return redirect("add_course")
        # if limit<5:
        #     messages.warning(request, "The course limit is full")
        #     return redirect("add_course")
        # print(course_name)
        course=Course(
            name=course_name,
        )
        course.save()
        messages.success(request, 'The Course is succesfully Added')
        return redirect('add_course')
    return render(request, 'Hod/add_course.html')
def courseenroll():
    pass
def VIEW_COURSE(request):
    course = Course.objects.all()
    print(course)
    context={
        'course':course,
    }
    return render(request,'Hod/view_course.html',context)
def EDIT_COURSE(request,id):
    course=Course.objects.get(id=id)
    context={
        'course':course,
    }
    return render(request, 'Hod/edit_course.html',context)
def UPDATE_COURSE(request):
    if request.method=="POST":
        name=request.POST.get('name')
        course_id=request.POST.get('course_id')
        course=Course.objects.get(id=course_id)
        course.name=name
        course.save()
        messages.success(request, 'Course Are Successfully Updated')
        return redirect("view_course")
    return render(request,'Hod/edit_course.html')


def DELETE_COURSE(request,id):
    course=Course.objects.get(id=id)
    course.delete()
    messages.success(request, "Course Are Successfully Deleted ")
    return redirect('view_course')
    
def ADD_STAFF(request):
    if request.method=="POST":
        profile_pic=request.FILES.get('profile_pic')
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        gender=request.POST.get('gender')
        email=request.POST.get('email')
        username=request.POST.get('username')
        password=request.POST.get('password')
        experience=request.POST.get('experience')
        address=request.POST.get('address')
        if CustomeUser.objects.filter(email=email).exists():
            messages.warning(request, 'Email Already Exists')
            return redirect('add_staff')
        if CustomeUser.objects.filter(username=username).exists():
            messages.warning(request, 'Username is already exist')
            redirect('add_staff')
        else:
            user=CustomeUser(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                profile_pic=profile_pic,
                user_type=2
            )
            user.set_password(password)
            user.save()
            staff=Staff(
                admin=user,
                address=address,
                gender=gender,
            )
            staff.save()
            messages.success(request, "Successfully Added")
            return redirect('add_staff')

    return render(request,'Hod/add_staff.html')
def VIEW_STAFF(request):
    staff=Staff.objects.all()
    context={
        'staff':staff,
    }
    return render(request, 'Hod/view_staff.html',context)
def EDIT_STAFF(request,id):
    staff=Staff.objects.filter(id=id)
    context={
        'staff':staff,
    }
    return render(request, 'Hod/edit_staff.html',context)
def UPDATE_STAFF(request):
    if request.method=="POST":
        staff_id=request.POST.get('staff_id')
        profile_pic=request.FILES.get('profile_pic')
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        gender=request.POST.get('gender')
        email=request.POST.get('email')
        username=request.POST.get('username')
        password=request.POST.get('password')
        experience=request.POST.get('experience')
        address=request.POST.get('address')
        user=CustomeUser.objects.get(id=staff_id)
        user.first_name=first_name
        user.last_name=last_name
        user.email=email
        user.username=username
        if profile_pic != None and profile_pic != "":
            user.profile_pic = profile_pic
        if password != None and password != "":
            user.set_password(password)
        user.save()
        staff=Staff.objects.get(admin=staff_id)
        staff.address=address
        staff.gender=gender
        staff.save()
        messages.success(request,'records are successfully updated')
        return redirect('view_staff')

def DELETE_STAFF(request,admin):
    staff=CustomeUser.objects.get(id=admin)
    staff.delete()
    messages.success(request,'Record are successfully deleted ! ')
    return redirect('view_staff')
def ADD_SESSION(request):
    if request.method=="POST":
        session_year_start=request.POST.get('session_year_start')
        session_year_end=request.POST.get('session_year_end')
        session=Session_Year(
            session_start=session_year_start,
            session_end=session_year_end,
        )
        session.save()
        messages.success(request, "Session Are Successfully Added!")
        return redirect('add_session')
    return render(request,'Hod/add_session.html')
def VIEW_SESSION(request):
    session=Session_Year.objects.all()
    context={
        'session':session,
    }
    return render(request, 'Hod/view_session.html',context)
def EDIT_SESSION(request,id):
    session=Session_Year.objects.filter(id=id)
    context={
        'session':session,
    }
    return render(request, 'Hod/edit_session.html',context)
def UPDATE_SESSION(request):
    if request.method=="POST":
        id_session=request.POST.get('id_session')
        session_year_start=request.POST.get('session_year_start')
        session_year_end=request.POST.get('session_year_end')
        session=Session_Year(
            id=id_session,
            session_start=session_year_start,
            session_end=session_year_end,
        )
        session.save()
        messages.success(request, "Successfully Updated")
        return redirect('view_session')
    return render(request, 'Hod/edit_session.html')
def DELETE_SESSION(request,id):
    session=Session_Year.objects.get(id=id)
    session.delete()
    messages.success(request, "Successfully Deleted")
    return redirect('view_session')

def ADD_SUBJECT(request):
    course=Course.objects.all()
    staff=Staff.objects.all()
    
    if request.method=="POST":
        subject_name=request.POST.get('subject_name')
        course_id=request.POST.get('course_id')
        staff_id=request.POST.get('staff_id')

        course=Course.objects.get(id=course_id)
        staff=Staff.objects.get(id=staff_id)
        if Subject.objects.filter(name=subject_name).exists():
            messages.warning(request, "Subject is already exist")
            return redirect("add_subject")
        subject=Subject(
            name=subject_name,
            course=course,
            staff=staff,
        )
        subject.save()
        messages.success(request, "Subject Are Successfully Added")
        return redirect('add_subject')
    context={
        'course':course,
        'staff':staff,
    }
    return render(request, 'Hod/add_subject.html',context)
def VIEW_SUBJECT(request):
    subject=Subject.objects.all()
    course=Course.objects.all()
    staff=Staff.objects.all()
    context={
        'subject':subject,
        'course':course,
        'staff':staff,
    }
    return render(request, 'Hod/view_subject.html',context)
def EDIT_SUBJECT(request,id):
    subject=Subject.objects.get(id=id)
    course=Course.objects.all()
    staff=Staff.objects.all()
    context={

        'subject':subject,
        'course':course,
        'staff':staff,
    }
    return render(request, 'Hod/edit_subject.html',context)
def UPDATE_SUBJECT(request):
    if request.method=="POST":
        subject_id=request.POST.get('subject_id')
        subject_name=request.POST.get('subject_name')
        course_id=request.POST.get('course_id')
        staff_id=request.POST.get('staff_id')
        
        course=Course.objects.get(id=course_id)
        staff=Staff.objects.get(id=staff_id)
        subject=Subject(
            id=subject_id,
            name=subject_name,
            course=course,
            staff=staff,

        )

        subject.save()
        messages.success(request, "Subject Are Successfully Updated")
        return redirect('view_subject')


    return render(request, 'Hod/edit_subject.html')
def DELETE_SUBJECT(request,id):
    subject=Subject.objects.get(id=id)
    subject.delete()
    messages.success(request, "Subject Are Successfully Deleted")
    return redirect('view_subject')

def STAFF_SEND_NOTIFICATION(request):
    staff=Staff.objects.all()
    see_notification=Staff_Notification.objects.all().order_by('-id')[0:5]
    context={
        'see_notification':see_notification,
        'staff':staff,
    }
    return render(request, 'Hod/send_staff_notification.html',context)
    
def SAVE_STAFF_NOTIFICATION(request):
    if request.method=="POST":
        staff_id=request.POST.get('staff_id')
        message=request.POST.get('message')
        staff=Staff.objects.get(admin=staff_id)
        notification=Staff_Notification(
            staff_id=staff,
            message=message,
        )
        notification.save()
        messages.success(request, 'Successfully Send Notification')
        return redirect('send_staff_notification')

def GENERATE(request):
    response=HttpResponse(content_type='text/plain')
    response['Content-Disposition']='attachment; filename=Student_Details.text'
    # Designate the model
    student=Student.objects.all()
    # Loop Through and output
    lines=[]
    for i in student:
        lines.append(f'This is the Student details\nThe name of the student is : {i}\n The Address of the student is:{i.address}\n')
    # lines=["This is line 1\n"
    # ,"This is line 2\n",
    # "This is line 3\n"]
    response.writelines(lines)
    return response


def student_leave_view(request):
    leaves = LeaveReportStudent.objects.all()
    context = {
        "leaves": leaves
    }
    return render(request, 'Hod/student_leave_view.html', context)

def student_leave_approve(request, leave_id):
    leave = LeaveReportStudent.objects.get(id=leave_id)
    leave.leave_status = 1
    leave.save()
    return redirect('student_leave_view')


def student_leave_reject(request, leave_id):
    leave = LeaveReportStudent.objects.get(id=leave_id)
    leave.leave_status = 2
    leave.save()
    return redirect('student_leave_view')


def staff_leave_view(request):
    leaves = LeaveReportStaff.objects.all()
    context = {
        "leaves": leaves
    }
    return render(request, 'Hod/staff_leave_view.html', context)


def staff_leave_approve(request, leave_id):
    leave = LeaveReportStaff.objects.get(id=leave_id)
    leave.leave_status = 1
    leave.save()
    return redirect('staff_leave_view')


def staff_leave_reject(request, leave_id):
    leave = LeaveReportStaff.objects.get(id=leave_id)
    leave.leave_status = 2
    leave.save()
    return redirect('staff_leave_view')
