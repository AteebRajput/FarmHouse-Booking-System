from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms import modelformset_factory
from .forms import FarmRegistrationForm, FarmImageForm
from .models import Farm, FarmImage
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from .forms import BookingForm,FarmSearchForm
from .models import Booking,Farm,FarmImage
import json


@login_required(login_url="login")
def register_farm(request):
    if request.method == 'POST':
        form = FarmRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            farm = form.save()
            images = request.FILES.getlist('images')
            for image in images:
                FarmImage.objects.create(farm=farm, image=image)
            return redirect('farm_list')
    else:
        form = FarmRegistrationForm()
    return render(request, 'farm/register_farm.html', {'form': form})


@login_required(login_url="login")
def farm_list(request):
    farms = Farm.objects.all()
    search_form = FarmSearchForm(request.GET or None)

    if search_form.is_valid():
        location = search_form.cleaned_data.get('location')
        farm_name = search_form.cleaned_data.get('farm_name')
        if location:
            farms = farms.filter(location=location)
        if farm_name:
            farms = farms.filter(name__icontains=farm_name)

    farms_with_images = []
    for farm in farms:
        primary_image = farm.images.first()
        farms_with_images.append({
            'farm': farm,
            'image': primary_image.image.url if primary_image else None
        })

    return render(request, 'farm/farm_list.html', {'farms': farms_with_images, 'search_form': search_form})




@login_required(login_url="login")
def farm_detail(request, farm_id):
    farm = get_object_or_404(Farm, id=farm_id)
    bookings = Booking.objects.filter(farm=farm)
    booked_dates = [(booking.check_in.strftime('%Y-%m-%d'), booking.check_out.strftime('%Y-%m-%d')) for booking in bookings]
    form = BookingForm()
    context = {
        'farm': farm,
        'form': form,
        'bookings': bookings,
        'booked_dates': json.dumps(booked_dates),
        'images': farm.images.all()
    }
    return render(request, 'farm/farm_detail.html', context)


@login_required(login_url="login")
def book_farm(request, farm_id):
    farm = get_object_or_404(Farm, id=farm_id)
    bookings = Booking.objects.filter(farm=farm)
    booked_dates = [(booking.check_in, booking.check_out) for booking in bookings]

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.farm = farm

           
            overlapping_bookings = bookings.filter(
                check_in__lt=booking.check_out, 
                check_out__gt=booking.check_in
            )
            if overlapping_bookings.exists():
                messages.error(request, 'The farm is already booked for the selected dates.')
            else:
                booking.save()
                messages.success(request, 'Your booking has been made successfully!')
                return redirect('farm_detail', farm_id=farm.id)
    else:
        form = BookingForm()

    context = {
        'farm': farm,
        'form': form,
        'bookings': bookings,
        'booked_dates': booked_dates,
    }
    return render(request, 'farm/book_farm.html', context)


'''
def register_farm(request):
    ImageFormSet = modelformset_factory(FarmImage, form=FarmImageForm, extra=3)  # Adjust extra as needed

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
            return redirect('/')  # Redirect to a page where the list of farms is displayed
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
    return render(request, 'farm/register_farm.html', context)
'''