from django import forms
from .models import Attendance_Report,Attendance,Student,Subject,Staff
ATTENDANCE_CHOICES=[
    ('Male','Male'),
    ('Female','Female')
]
P=1
A=0
ATTENDANCE_OPTION=(
    (P,'Present'),
    (A,'Absent')
)
class Attendance_Form(forms.ModelForm):
    class Meta:
        model=Attendance_Report
        fields=['student_id','attendance_id']
        labels={
            'student_id':'Student ID',
            'attendance_id':'Attendance ID'
        }
class TakeAttendance(forms.ModelForm):
    mark=forms.ChoiceField(choices=ATTENDANCE_OPTION,widget=forms.RadioSelect)
    # student=forms.MultipleChoiceField(queryset=Student.objects.all())
    class Meta:
        model=Attendance
        fields=['student_id',"subject_id","attendance_date","mark"]
        labels={'student_id':"Student Name","subject_id":'Subject Name','attendance_date':"Select Date","mark":"Mark Attendance"}
        widgets = {
                'student_id':forms.CheckboxSelectMultiple(),

    # 'student_id':forms.Select(attrs={'class':'form-control'}),
    'subject_id':forms.Select(attrs={'class':'form-control'}),
    'attendance_date': forms.DateInput(format=('%d-%m-%Y'), attrs={'class':'form-control','firstDay': 1, 'pattern=': '\d{4}-\d{2}-\d{2}', 'lang': 'pl', 'format': 'yyyy-mm-dd', 'type': 'date'},
    
    ),

        }  

