import imp
from re import template
from typing import List
from unicodedata import category
from urllib import request
from django.shortcuts import render, get_object_or_404, HttpResponse
from .models import Room, RoomImage, Staff, HotelImage
from django.views.generic import ListView, DetailView, FormView, View
from blog.models import Post
from .forms import AvailabilityForm




class HomeView(ListView):
    model = Room
    template_name = 'app/home.html'
    context_object_name = "rooms"
    extra_context={'staffs': Staff.objects.all(), 'posts': Post.objects.all()}


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