# admin_interface/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from farmhouse.models import Farm, Booking, FarmImage
from farmhouse.forms import FarmRegistrationForm,FarmImageForm
from django.forms import modelformset_factory
from .forms import UserUpdateForm,AdminBookingForm
from django.contrib.auth.models import User
from django.contrib import messages
from farmhouse.decorators import admin_only
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect,HttpResponse
from accounts.models import Profile
import uuid
from accounts.utils import *
import logging


@login_required
@admin_only
def admin_dashboard(request):
    total_farms = Farm.objects.count()
    total_customers = User.objects.count()
    total_bookings = Booking.objects.count()

    context = {
        'total_farms': total_farms,
        'total_customers': total_customers,
        'total_bookings': total_bookings,
    }
   
    return render(request, 'admin_interface/admin_dashboard.html',context)

@login_required
@admin_only
def admin_farm_list(request):
    farms_with_images = []
    farms = Farm.objects.all()  
    for farm in farms:
        primary_image = farm.images.first()
        farms_with_images.append({
            'farm': farm,
            'image': primary_image.image.url if primary_image else None
        })

    return render(request, 'admin_interface/admin_farm_list.html', {'farms_with_images': farms_with_images})


@login_required
@admin_only
def admin_farm_detail(request, pk):
    farm = get_object_or_404(Farm, pk=pk)
    images = FarmImage.objects.filter(farm=farm)
    bookings = Booking.objects.filter(farm=farm)
    return render(request, 'admin_interface/admin_farm_detail.html', {'farm': farm, 'images': images, 'bookings': bookings})

@login_required
@admin_only
def admin_update_farm(request, pk):
    farm = get_object_or_404(Farm, pk=pk)
    if request.method == 'POST':
        form = FarmRegistrationForm(request.POST, request.FILES, instance=farm)
        if form.is_valid():
            form.save()
            images = request.FILES.getlist('images')
            for image in images:
                FarmImage.objects.create(farm=farm, image=image)
            return redirect('admin_farm_detail', pk=farm.pk)
    else:
        form = FarmRegistrationForm(instance=farm)
    return render(request, 'admin_interface/admin_update_farm.html', {'form': form})

@login_required
@admin_only
def admin_delete_farm(request, pk):
    farm = get_object_or_404(Farm, pk=pk)
    if request.method == 'POST':
        farm.delete()
        return redirect('admin_farm_list')
    return render(request, 'admin_interface/admin_delete_farm.html', {'farm': farm})

@login_required
@admin_only
def admin_user_list(request):
    users = User.objects.all()
    user_data = []

    for user in users:
        total_bookings = Booking.objects.filter(user=user).count()
        user_data.append({
            'user': user,
            'total_bookings': total_bookings,
        })

    context = {
        'user_data': user_data,
    }
    return render(request, 'admin_interface/admin_user_list.html', context)

@login_required
@admin_only
def admin_update_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'User updated successfully.')
            return redirect('admin_user_list')
    else:
        form = UserUpdateForm(instance=user)
    return render(request, 'admin_interface/admin_update_user.html', {'form': form})


@login_required
@admin_only
def admin_delete_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('admin_user_list')
    return render(request, 'admin_interface/admin_delete_user.html', {'user': user})

@login_required
@admin_only
def admin_booking_list(request):
    bookings = Booking.objects.all()
    return render(request, 'admin_interface/admin_booking_list.html', {'bookings': bookings})

@login_required
@admin_only
def admin_cancel_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    booking.order_status = 'canceled'
    booking.save()
    return redirect('admin_booking_list')


@login_required
@admin_only
def register_farm(request):
    ImageFormSet = modelformset_factory(FarmImage, form=FarmImageForm, extra=3)  

    if request.method == 'POST':
        form = FarmRegistrationForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES, queryset=FarmImage.objects.none())

        if form.is_valid() and formset.is_valid():
            farm = form.save(commit=False)
            farm.owner = request.user
            farm.save()

            for form in formset.cleaned_data:
                if form:
                    image = form['image']
                    photo = FarmImage(farm=farm, image=image)
                    photo.save()

            messages.success(request, 'Your farm and images have been registered successfully!')
            return redirect('admin_farm_list') 
        else:
            print(form.errors)
            print(formset.errors)
            messages.error(request, 'There was an error in your form.')

    else:
        form = FarmRegistrationForm()
        formset = ImageFormSet(queryset=FarmImage.objects.none())

    context = {
        'form': form,
        'formset': formset,
    }
    return render(request, 'admin_interface/register_farm.html', context)


@login_required
@admin_only
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
            return redirect("admin_user_list")
        else:
            logger.error(f"Failed to send email to {email}")
            messages.error(request, 'There was an error sending the email.')

        return HttpResponseRedirect(request.path_info)

    return render(request, 'admin_interface/register_user.html')


@login_required
@admin_only
def admin_create_booking(request):
    form = AdminBookingForm()  
    if request.method == "POST":
        form = AdminBookingForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Booking created successfully.')
            return redirect('admin_dashboard')  
    return render(request, 'admin_interface/admin_create_booking.html', {'form': form})
