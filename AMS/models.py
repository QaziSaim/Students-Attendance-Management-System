from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class CustomeUser(AbstractUser):
    USER=(
        (1,'HOD'),
        (2,'STAFF'),
        (3,'STUDENT')


    )
    user_type=models.CharField(choices=USER,max_length=50,default=1)
    profile_pic=models.ImageField(upload_to='media/profile_pic')
class Course(models.Model):
    name=models.CharField(max_length=100)
    limit=models.PositiveIntegerField(default=5)
    create_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)

    def can_register(self):
        return self.limit>self.__class__.objects.count()

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
    # dob=models.CharField(max_length=100)
    course_id=models.ForeignKey(Course,on_delete=models.DO_NOTHING)
    session_year_id=models.ForeignKey(Session_Year,on_delete=models.DO_NOTHING)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)

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

# Attendance Model

class Attendance(models.Model):
    student_id=models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    subject_id=models.ForeignKey(Subject, on_delete=models.DO_NOTHING)
    attendance_date=models.DateField()
    mark=models.IntegerField(default=0)
    # staff_username=models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

class Attendance_Report(models.Model):
    ATTENDANCE_CHOICES = (
        ('A', 'Absent'),
        ('P', 'Present'),
        ('L', 'Late'),
    )
    student_id=models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    attendance_id=models.ForeignKey(Attendance, on_delete=models.CASCADE)
    attendance_status = models.CharField(max_length=1, choices=ATTENDANCE_CHOICES)



    def __str__(self):
        return self.student_id.admin.first_name

    
