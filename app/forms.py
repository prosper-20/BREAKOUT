import email
from logging import PlaceHolder
import re
from django import forms
from .models import Category, Message, HomeBooking
from django.conf import settings



class AvailabilityForm(forms.Form):
    ROOM_CATEGORIES = (
        ('ST', 'STANDARD'),
        ('EXE', 'EXECUTIVE'),
        ('BUS', 'BUSINESS'),
        ('PRE', 'PREMIUM'),
        ('DEL', 'DELUXE'),
        ('PNT', 'PENTHOUSE'),
        ('KN', 'KING')

    )
    # name = forms.CharField(help_text="Enter a username")
    # email = forms.EmailField(help_text="Enter a valid email address")
    room_category = forms.ChoiceField(choices=ROOM_CATEGORIES, required=True)
    check_in = forms.DateTimeField(required=True, input_formats=["%Y-%m-%dT%H:%M", ])
    check_out = forms.DateTimeField(required=True, input_formats=["%Y-%m-%dT%H:%M", ])



# You created this for the contact form

class ContactForm(forms.ModelForm):
    class Meta:
        model = Message

        fields = ["name", "email", "message"]


class HotelBookingForm(forms.ModelForm):
    class Meta:
        model = HomeBooking


        fields = ["check_in", "check_out", "adults", "room", "email", "phone"]