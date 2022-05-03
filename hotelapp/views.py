from audioop import reverse
from django.urls import reverse, reverse_lazy
from typing import List
from django.shortcuts import render, HttpResponse
from django.views.generic import ListView, FormView, View, DeleteView
from .forms import AvailabilityForm 
from .models import Room, Booking
from hotelapp.booking_functions.availability import check_availability
from hotelapp.booking_functions.get_room_cat_url_list import get_room_cat_url_list
from hotelapp.booking_functions.get_room_category_human_format import get_room_category_human_format
from hotelapp.booking_functions.get_available_rooms import get_available_rooms
from hotelapp.booking_functions.book_room import book_room
# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

def RoomListView(request):
    room_category_url_list = get_room_cat_url_list()
    # rooms = Room.objects.all()
    rooms = Room.objects.filter(category=room_category_url_list[0][0])
    context = {
        "room_list": room_category_url_list,
        "rooms": rooms
    }
    return render(request, 'app/our_room.html', context)
    #return render(requsest, 'hotel/room_list_view.html', context)


class BookingListView(ListView):
    model = Booking
    template_name = "hotel/booking_list_view.html"
    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_staff:
            booking_list = Booking.objects.all()
            return booking_list
        else:
            booking_list = Booking.objects.filter(user=self.request.user)
            return booking_list


class RoomDetailView(LoginRequiredMixin, View):
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
            # You changed form hotrl/room_detail_view.html
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


class CancelBookingView(DeleteView):
    model = Booking
    template_name = "hotel/booking_cancel_view.html"
    success_url = reverse_lazy('BookingListView')

# class BookingView(FormView):
#     form_class = AvailabilityForm
#     template_name="hotel/availability_form.html"

#     def form_valid(self, form):
#         data = form.cleaned_data
#         room_list = Room.objects.filter(category=data['room_category'])
#         available_rooms = []
#         for room in room_list:
#             if check_availability(room, data['check_in'], data['check_out']):
#                 available_rooms.append(room)

#         if len(available_rooms) > 0:
#             room = available_rooms[0]
#             booking = Booking.objects.create(
#                 user=self.request.user,
#                 room=room,
#                 check_in=data['check_in'],
#                 check_out=data['check_out']
#             )
#             booking.save()
#             return HttpResponse(booking)
#         else:
#             return HttpResponse("This category of rooms are fully booked!")
