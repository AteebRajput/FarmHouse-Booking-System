
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect,HttpResponse
from .models import Profile
import uuid
from accounts.utils import *
import logging

logger = logging.getLogger(__name__)

def login_page(request):
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username = email)

        if not user_obj.exists():
            messages.warning(request, 'Account not found.')
            return HttpResponseRedirect(request.path_info)
        
        if not user_obj[0].profile.is_email_verified:
            messages.warning(request, 'Your account is not verified.')
            return HttpResponseRedirect(request.path_info)

        user_obj = authenticate(username = email , password= password)
        if user_obj:
            login(request , user_obj)
            return redirect('farm_list')

        messages.warning(request, 'Invalid credentials')
        return HttpResponseRedirect(request.path_info)

    return render(request ,'accounts/login.html')


def login_admin(request):
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username = email)

        if not user_obj.exists():
            messages.warning(request, 'Account not found.')
            return HttpResponseRedirect(request.path_info)
        
        if not user_obj[0].profile.is_email_verified:
            messages.warning(request, 'Your account is not verified.')
            return HttpResponseRedirect(request.path_info)

        user_obj = authenticate(username = email , password= password)
        if user_obj:
            login(request , user_obj)
            return redirect('admin_dashboard')

        messages.warning(request, 'Invalid credentials')
        return HttpResponseRedirect(request.path_info)

    return render(request ,'accounts/admin_login.html')


def register_page(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username=email)
        if user_obj.exists():
            messages.warning(request, 'Email is already taken.')
            return HttpResponseRedirect(request.path_info)

        user_obj = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=email
        )
        user_obj.set_password(password)
        user_obj.save()
        group = Group.objects.get(name = 'customer')
        user_obj.groups.add(group)
        profile_obj = Profile.objects.create(
            user=user_obj,
            email_token=str(uuid.uuid4())
        )
        if send_account_activation_email(email, profile_obj.email_token):
            messages.success(request, 'An email has been sent to your email address.')
        else:
            logger.error(f"Failed to send email to {email}")
            messages.error(request, 'There was an error sending the email.')

        return HttpResponseRedirect(request.path_info)

    return render(request, 'accounts/register.html')

def register_admin(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username=email)
        if user_obj.exists():
            messages.warning(request, 'Email is already taken.')
            return HttpResponseRedirect(request.path_info)

        user_obj = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=email
        )
        user_obj.set_password(password)
        user_obj.save()
        
        group = Group.objects.get(name='admin')
        user_obj.groups.add(group)

        profile_obj = Profile.objects.create(
            user=user_obj,
            email_token=str(uuid.uuid4())
        )
        
        if send_account_activation_email(email, profile_obj.email_token):
            messages.success(request, 'An email has been sent to your email address.')
        else:
            messages.error(request, 'There was an error sending the email.')

        return HttpResponseRedirect(request.path_info)

    return render(request, 'accounts/register_admin.html')



def my_logout(request):
    auth_logout(request)
    return redirect('login')


def activate_email(request , email_token):
    try:
        user = Profile.objects.get(email_token= email_token)
        user.is_email_verified = True
        user.save()
        return redirect('farm_list')
    except Exception as e:
        return HttpResponse('Invalid Email token')
    