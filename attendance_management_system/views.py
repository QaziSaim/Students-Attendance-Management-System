from django.contrib.auth.models import User, auth
from django.shortcuts import render,redirect,HttpResponse
from AMS.EmailBackEnd import EmailBackEnd
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from AMS.models import CustomeUser

def BASE(request):
    return render(request,'base.html')
def LOGIN(request):
    return render(request,'login.html')
def doLogin(request):
    if request.method == "POST":
        user=EmailBackEnd.authenticate(request,username=request.POST.get('email'),
                                       password=request.POST.get('password'),
                                       )
        if user!=None:
            login(request,user)
            user_type=user.user_type
            if user_type=='1':
                # return HttpResponse('This is HOD panel')
                return redirect('hod_home')
                # pass
            elif user_type=='2':
                return redirect('staff_home')
                # pass
            elif user_type=='3':
                return redirect('student_home')
                # pass
            else:
                #Message
                messages.error(request,'Invalid Credentials !')
                return redirect('login')

        else:
            messages.error(request,'Invalid Credentials !')
            return redirect('login')



def doLogout(request):
    logout(request)
    return redirect('login')
@login_required(login_url='/')
def profile(request):
    user=CustomeUser.objects.get(id = request.user.id)
    context={
        "user":user,
    }
    return render(request, 'profile.html')
@login_required(login_url='/')
def PROFILE_UPDATE(request):
    if request.method=="POST":
        profile_pic=request.FILES.get('profile_pic')
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        password=request.POST.get('password')
        # print(profile_pic,first_name,last_name,email,username,password)
        try:
            customeuser=CustomeUser.objects.get(id=request.user.id)
            customeuser.first_name=first_name
            customeuser.last_name=last_name
            if profile_pic !=None and profile_pic !="":
                customeuser.profile_pic=profile_pic
            if password !=None and password !="":
                customeuser.set_password(password)
            customeuser.save()
            messages.success(request,'Your Profile Update Successfully')
            redirect('profile')
        except:
            messages.error(request,'Your Profile Not Updated')

    return render(request,'profile.html')

