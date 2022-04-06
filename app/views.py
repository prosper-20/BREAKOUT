import imp
from re import template
from typing import List
from unicodedata import category
from urllib import request
from django.shortcuts import render, get_object_or_404, HttpResponse
from .models import Room, RoomImage, Staff, Booking, HotelImage
from django.views.generic import ListView, DetailView, FormView, View
from blog.models import Post
from .forms import AvailabilityForm
from app.booking_functions.availability import check_availability



class HomeView(ListView):
    model = Room
    template_name = 'app/home.html'
    context_object_name = "rooms"
    extra_context={'staffs': Staff.objects.all(), 'posts': Post.objects.all()}

class BookingList(ListView):
    model = Booking

# def tester(request, slug):
#     room = get_object_or_404(Room, slug=slug)
#     form = AvailabilityForm()
#     context = {
#         "room": room,
#         "form": form
#     }
#     return render(request, 'app/room_booking.html', context)



class BookingView(FormView):
    form_class = AvailabilityForm
    template_name = 'app/availability_form.html'
    extra_context = {"form": AvailabilityForm}

    def form_valid(self, form):
        data = form.cleaned_data
        room_list = Room.objects.filter(category=data['room_category'])
        available_rooms = []
        for room in room_list:
            if check_availability(room, data['check_in'], data['check_out']):
                available_rooms.append(room)

        if len(available_rooms) > 0:
            room = available_rooms[0]
            booking = Booking.objects.create(
                user=self.request.user,
                room=room,
                check_in=data['check_in'],
                check_out=data['check_out']
            )
            booking.save()
            return HttpResponse(booking)
        else:
            return HttpResponse('All of this category of rooms are booked!! Try another one')
            



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
    return render(request, "app/news.html", context)