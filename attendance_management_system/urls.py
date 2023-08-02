
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .import staff_views, Hod_views, Student_Views, views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('base/', views.BASE,name='base'),
    # Login Path
    path('', views.LOGIN,name='login'),
    path("doLogout", views.doLogout,name='logout'),
    path('doLogin', views.doLogin,name='doLogin'),
    # Profile Update
    path('profile', views.profile, name='profile'),
    path('Profile/update',views.PROFILE_UPDATE,name='profile_update'),

    #HOD home page
    path('Hod/home', Hod_views.home,name='hod_home'),
    # Student Page
    path('Hod/Student/Add',Hod_views.ADD_STUDENT,name='add_student'),
    path('Hod/Student/View',Hod_views.VIEW_STUDENT,name='view_student'),
    path('Hod/Student/Edit/<str:id>',Hod_views.EDIT_STUDENT,name='edit_student'),
    path('Hod/Student/Update',Hod_views.UPDATE_STUDENT,name='update_student'),
    path('Hod/Student/Delete/<str:admin>',Hod_views.DELETE_STUDENT,name='delete_student'),
    path('Hod/Student/generate',Hod_views.GENERATE,name='generate'),

    #Staff Page
    path('Hod/Staff/Add',Hod_views.ADD_STAFF,name='add_staff'),
    path('Hod/Staff/View',Hod_views.VIEW_STAFF,name='view_staff'),
    path('Hod/Staff/Edit/<str:id>',Hod_views.EDIT_STAFF,name='edit_staff'),
    path('Hod/Staff/Update',Hod_views.UPDATE_STAFF,name='update_staff'),
    path('Hod/Staff/Delete/<str:admin>',Hod_views.DELETE_STAFF,name='delete_staff'),
    path('student_leave_view/', Hod_views.student_leave_view, name="student_leave_view"),
    path('student_leave_approve/<leave_id>/', Hod_views.student_leave_approve, name="student_leave_approve"),
    path('student_leave_reject/<leave_id>/', Hod_views.student_leave_reject, name="student_leave_reject"),
    path('staff_leave_view/', Hod_views.staff_leave_view, name="staff_leave_view"),
    path('staff_leave_approve/<leave_id>/', Hod_views.staff_leave_approve, name="staff_leave_approve"),
    path('staff_leave_reject/<leave_id>/', Hod_views.staff_leave_reject, name="staff_leave_reject"),

    # Course
    path('Hod/Course/Add',Hod_views.ADD_COURSE,name='add_course'),
    path('Hod/Course/View',Hod_views.VIEW_COURSE,name='view_course'),
    path('Hod/Course/Edit/<str:id>',Hod_views.EDIT_COURSE,name='edit_course'),
    path('Hod/Course/Update',Hod_views.UPDATE_COURSE,name='update_course'),
    path('Hod/Course/Delete/<str:id>',Hod_views.DELETE_COURSE,name='delete_course'),

    #Session
    path('Hod/Session/Add',Hod_views.ADD_SESSION,name='add_session'),
    path('Hod/Session/View',Hod_views.VIEW_SESSION,name='view_session'),
    path('Hod/Session/Edit/<str:id>',Hod_views.EDIT_SESSION,name='edit_session'),
    path('Hod/Session/Update',Hod_views.UPDATE_SESSION,name='update_session'),
    path('Hod/Session/Delete/<str:id>',Hod_views.DELETE_SESSION,name='delete_session'),
    path('Hod/Course/enroll',Hod_views.courseenroll,name='course_enroll'),
    #Subject 
    path('Hod/Subject/Add',Hod_views.ADD_SUBJECT,name='add_subject'),
    path('Hod/Subject/View',Hod_views.VIEW_SUBJECT,name='view_subject'),
    path('Hod/Subject/Edit/<str:id>',Hod_views.EDIT_SUBJECT,name='edit_subject'),
    path('Hod/Subject/Update',Hod_views.UPDATE_SUBJECT,name='update_subject'),
    path('Hod/Subject/Delete/<str:id>',Hod_views.DELETE_SUBJECT,name='delete_subject'),

    #Send Staff Notification
    path('Hod/Staff/Send_Notification',Hod_views.STAFF_SEND_NOTIFICATION,name='send_staff_notification'),
    path("Hod/Staff/Save_Notitication",Hod_views.SAVE_STAFF_NOTIFICATION,name='save_staff_notification'),

    #This is staff urls
    path('Hod/Staff',staff_views.HOME,name='staff_home'),
    path('Staff/attendance', staff_views.STAFF_TAKE_ATTENDANCE, name='staff_take_attendance'),
    path('Staff/records', staff_views.STAFF_SAVE_ATTENDANCE, name='staff_save_attendance'),
    path('Staff/viewStudAtten', staff_views.STAFF_VIEW_ATTENDANCE, name='staff_view_attendance'),
    path('Staff/Attendance',staff_views.take_attendance,name='attendance'),
    path('Staff/Attendance/Present',staff_views.PRESENT_REPORT,name='present_report'),
    path('staff_apply_leave/', staff_views.staff_apply_leave, name="staff_apply_leave"),
    path('staff_apply_leave_save/', staff_views.staff_apply_leave_save, name="staff_apply_leave_save"),
    
    #This is Student urls
    path('Hod/Student',Student_Views.HOME,name='student_home'),
    path('send-sms/<str:date>/', staff_views.send_sms, name='send_sms'),
    path('student_apply_leave/', Student_Views.student_apply_leave, name="student_apply_leave"),
    path('student_apply_leave_save/', Student_Views.student_apply_leave_save, name="student_apply_leave_save"),
    
    


]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
