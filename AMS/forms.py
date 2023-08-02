from django import forms
from .models import Attendance_Report,Attendance,Student,Subject,Staff
from django.forms.widgets import CheckboxSelectMultiple
from datetime import date
P=1
A=0
ATTENDANCE_OPTION=(
    (P,'Present'),
    (A,'Absent')
)
class TakeAttendance(forms.ModelForm):
    mark=forms.ChoiceField(choices=ATTENDANCE_OPTION,widget=forms.RadioSelect)
    student_id=forms.ModelMultipleChoiceField(queryset=Student.objects.all(),widget=CheckboxSelectMultiple,)
    class Meta:
        model=Attendance
        fields=['student_id',"subject_id","attendance_date","mark"]
        labels={'student_id':"Student Name","subject_id":'Subject Name','attendance_date':"Select Date","mark":"Mark Attendance"}
        widgets = {
    'subject_id':forms.Select(attrs={'class':'form-control'}),
    'attendance_date': forms.DateInput(
                format=('%d-%m-%Y'),
                attrs={
                    'class': 'form-control',
                    'min': date.today().strftime('%Y-%m-%d'),
                    'max': date.today().strftime('%Y-%m-%d'),
                    'type': 'date'
                })}  

ATTENDANCE_CHOICES=[
    ('Male','Male'),
    ('Female','Female')
]
class Attendance_Form(forms.ModelForm):
    class Meta:
        model=Attendance_Report
        fields=['student_id','attendance_id']
        labels={
            'student_id':'Student ID',
            'attendance_id':'Attendance ID'
        }