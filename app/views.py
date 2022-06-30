from email import message
import imp
from operator import pos
from re import template
from typing import List
from unicodedata import category
from urllib import request
from django.shortcuts import render, get_object_or_404, HttpResponse
from .models import Room, RoomImage, Staff, HotelImage, Message
from django.views.generic import ListView, DetailView, FormView, View
from blog.models import Post
from .forms import AvailabilityForm, ContactForm
from hotelapp.booking_functions.get_room_category_human_format import get_room_category_human_format

from hotelapp.booking_functions.get_available_rooms import get_available_rooms
from hotelapp.booking_functions.book_room import book_room
from hotelapp.booking_functions.get_room_cat_url_list import get_room_cat_url_list

# For Contact Email Sending
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import auth, User
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from django.core.mail import EmailMessage, send_mail
from sendgrid.helpers.mail import SandBoxMode, MailSettings
from .models import HomeBooking
from .forms import HotelBookingForm


# class HomeView(ListView):
#     model = Room
#     template_name = 'app/home.html'
#     context_object_name = "rooms"
#     extra_context={'staffs': Staff.objects.all(), 'posts': Post.objects.all()}


def HomeView(request):
    room_category_url_list = get_room_cat_url_list()
    rooms = Room.objects.filter(category=room_category_url_list[0][0])
    room = Room.objects.all()
    staffs = Staff.objects.all()
    posts = Post.objects.all()
    template_name = "app/home.html"
    context = {
        "room": room,
        "staffs": staffs,
        "posts": posts,
        "room_list": room_category_url_list,
        "rooms": rooms
    }
    # THIS IS WHERE YOU STARTED ADDING THINGS FOR THE FORM ON THE 1ST PAGE
    if request.method == 'POST':
        check_in = request.POST["check_in"]
        check_out = request.POST["check_out"]
        adults = request.POST["adults"]
        room = request.POST["room"]
        email = request.POST["email"]
        phone = request.POST["phone"]


        user_booking = HomeBooking.objects.create(check_in=check_in,
        check_out=check_out, adults=adults, room=room, email=email,
        phone=phone)
        user_booking.save()
        mydict = {'check_in': check_in, 'check_out': check_out, 'adults': adults, 'room': room, 'email': email, 'phone': phone}
        # FOR SENDING AUTO MAILS
        html_template = 'app/main_email.html'
        html_message = render_to_string(html_template, context=mydict)
        subject = 'Room Reservation'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]
        message = EmailMessage(subject, html_message,
                                email_from, recipient_list)
        message.content_subtype = 'html'
        message.send()
        messages.success(request, "Reservation has been placed")
        return redirect("home")
    else:
        return render(request, template_name, context)


class RoomDetailView(DetailView):
    model = Room
    


def detail_view(request, slug):
    room = get_object_or_404(Room, slug=slug)
    photos = RoomImage.objects.filter(room=room)
    return render(request, 'app/room_detail.html', {
        'room':room,
        'photos':photos
    })

def contact(request):
    return render(request, "app/contact-us.html")


def about(request):
    staffs = Staff.objects.all()
    context = {"staffs": staffs}
    return render(request, "app/about-us.html", context)


def search_rooms(request):
    if request.method == "POST":
        searched = request.POST['searched']
        # This returns the results of the user's search
        rooms = Room.objects.filter(slug__contains=searched)
        # return render(request, "app/rooms_search.html", {'searched': searched, 'rooms': rooms})
        return render(request, "app/search_rooms.html", {'searched': searched, 'rooms': rooms})
    else:
        return render(request, "app/search_rooms.html")



def gallery(request):
    images =  HotelImage.objects.all()
    context = {
        "images": images
    }
    return render(request, 'app/gallery.html', context)


def news(request):
    posts = Post.objects.all()
    context = {
        "posts": posts
    }
    return render(request, "blog/news.html", context)

def staff(request):
    staffs = Staff.objects.all()
    context = {
        'staffs': staffs
    }
    return render(request, 'app/staff.html', context)

def rooms(request):
    rooms = Room.objects.all()
    context = {
        'rooms': rooms
    }
    return render(request, "app/our_room.html", context)



# You created this to test the booking


class TestView(View):
    def get(self, request, *args, **kwargs):
        category = self.kwargs.get('category', None)

        # Get the human raedable formst
        human_format_room_category = get_room_category_human_format(category)
        form = AvailabilityForm() # Initialisze empty form
        # You just added this
        room = Room.objects.filter(category=category).first()
        room_cap = Room.objects.filter(capacity=1)
        if human_format_room_category is not None: # check for invalid category names
            context = {
                'room_category': human_format_room_category,
                "form": form,
                "room": room #new
            }
            return render(request, 'app/room_booking.html', context)
        else:
            return HttpResponse('Category does not exist')

    def post(self, request, *args, **kwargs):
        category = self.kwargs.get('category', None) #Get room category from kwargs
        
        form = AvailabilityForm(request.POST) # pass request.POST into AvailabilityForm
        if form.is_valid():
            data = form.cleaned_data

        available_rooms = get_available_rooms(category, data['check_in'], data['check_out'])

        if available_rooms is not None:
            booking = book_room(request, available_rooms[0], data['check_in'], data['check_out'])
            return HttpResponse(booking)
        else:
            return HttpResponse("This category of rooms are fully booked!")




# def contact_us(request):
#     if request.method == 'POST':
#         form = ContactForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get("name")
#             email = form.cleaned_data.get("email")
#             message = form.cleaned_data.get("message")
#             form.save()
#             mydict = {'username': username, 'email':email, 'message': message}
#             mail_settings = MailSettings()
#             mail_settings.sandbox_mode = SandBoxMode(False)
#             html_template = 'app/contact_email.html'
#             html_message = render_to_string(html_template, context=mydict)
#             subject = 'Welcome to Service-Verse'
#             email_from = settings.EMAIL_HOST_USER
#             recipient_list = [email]
#             message = EmailMessage(subject, html_message,
#                                    email_from, recipient_list)
#             message.content_subtype = 'html'
#             message.send()
#             return redirect("/")
#     else:
#         form = ContactForm()
#     context = {
#         'form': form
#     }
#     # changed from contact_us_2.html
#     return render(request, 'app/contact_us_2.html', context)


def contact_us(request):
    if request.method == "POST":
        username = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']

        new = Message.objects.create(name=username, email=email,
        message=message)
        new.save()
        mydict = {'username': username, 'email':email, 'message': message}
        mail_settings = MailSettings()
        mail_settings.sandbox_mode = SandBoxMode(False)
        html_template = 'app/contact_email.html'
        html_message = render_to_string(html_template, context=mydict)
        subject = 'Welcome to Service-Verse'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]
        message = EmailMessage(subject, html_message,
                                email_from, recipient_list)
        message.content_subtype = 'html'
        message.send()
        return redirect("/")

    else:
        return render(request, 'app/contact-us.html')
            


def homebooking(request):
    if request.method == "POST":
        form = HotelBookingForm(request.POST)
        if form.is_valid():
            check_in = form.cleaned_data.get("check_in")
            check_out = form.cleaned_data.get('check_out')
            adults = form.cleaned_data.get("adults")
            room = form.cleaned_data.get("room")
            email = form.cleaned_data.get("email")
            phone = form.cleaned_data.get("phone")

            form.save()
            messages.success(request, f"A message has been sent to your mail.")
            return redirect("home")
            # check_in = request.POST["check_in"]
            # check_out = request.POST["check_out"]
            # adults = request.POST["adults"]
            # room = request.POST["room"]
            # email = request.POST["email"]
            # phone = request.POST["phone"]


            # user_booking = homebooking.objects.create(check_in=check_in,
            # check_out=check_out, adults=adults, room=room, email=email,
            # phone=phone)
            # user_booking.save()
    else:
        form = HotelBookingForm()
    return render(request, "app/home_booking.html", {'form': form})



def personal(request):
    return render(request, 'app/personal_info.html')

