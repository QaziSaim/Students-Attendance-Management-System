from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
# The entire database 
# class tablename
class CustomeUser(AbstractUser):
    USER=(
        (1,'HOD'),
        (2,'STAFF'),
        (3,'STUDENT')


    )
    user_type=models.CharField(choices=USER,max_length=50,default=1)
    profile_pic=models.ImageField(upload_to='media/profile_pic')
class Course(models.Model):
    name=models.CharField(max_length=100,null=False)
    create_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    limit=models.PositiveIntegerField(default=5)
    def __str__(self):
        return self.name
class Session_Year(models.Model):
    session_start=models.CharField(max_length=100)
    session_end=models.CharField(max_length=100)

    def __str__(self):
        return self.session_start+" TO "+ self.session_end
class Student(models.Model):
    admin=models.OneToOneField(CustomeUser,on_delete=models.CASCADE)
    address=models.TextField()
    gender=models.CharField(max_length=100)
    course_id=models.ForeignKey(Course,on_delete=models.DO_NOTHING)
    session_year_id=models.ForeignKey(Session_Year,on_delete=models.DO_NOTHING)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    phone_number=models.PositiveIntegerField() 

    def __str__(self):
        return self.admin.first_name+ " "+ self.admin.last_name
class Staff(models.Model):
    admin=models.OneToOneField(CustomeUser, on_delete=models.CASCADE)
    address=models.TextField()
    gender=models.CharField(max_length=200)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.admin.first_name+ " "+ self.admin.last_name
class Subject(models.Model):
    name=models.CharField(max_length=100)
    course=models.ForeignKey(Course, on_delete=models.CASCADE)
    staff=models.ForeignKey(Staff, on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True,null=True)
    updated_at=models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return self.name
class Staff_Notification(models.Model):
    staff_id=models.ForeignKey(Staff, on_delete=models.CASCADE)
    message=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    stauts=models.IntegerField(null=True,default=0)

    def __str__(self):
        return self.staff_id.admin.first_name
class Staff_leave(models.Model):
    staff_id=models.ForeignKey(Staff, on_delete=models.CASCADE)
    data=models.CharField(max_length=100)
    message=models.TextField()
    status=models.IntegerField(default=0)
    created_at=models.DateTimeField(auto_now_add=True)
    Updated_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.staff_id.admin.first_name
    
class Class(models.Model):
    staff=models.ForeignKey(Staff, on_delete=models.CASCADE)
    session_year=models.ForeignKey(Session_Year, on_delete=models.CASCADE,null=True,default="Free")
    
    name=models.CharField(max_length=250)
    level = models.CharField(max_length=250)

    def __str__(self):
        return self.name


# Attendance Model
class Attendance(models.Model):
    subject_id=models.ForeignKey(Subject, on_delete=models.DO_NOTHING)
    attendance_date=models.DateField()
    student_id=models.ManyToManyField(Student)
    mark=models.IntegerField(default=0)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return self.subject_id.name
class Attendance_Report(models.Model):
    student_id=models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    attendance_id=models.ForeignKey(Attendance, on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    stauts=models.IntegerField(null=True,default=0) 

    def __str__(self):
        return self.student_id.admin.first_name

class LeaveReportStudent(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    leave_date = models.CharField(max_length=255)
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class LeaveReportStaff(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Staff, on_delete=models.CASCADE)
    leave_date = models.CharField(max_length=255)
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


    
