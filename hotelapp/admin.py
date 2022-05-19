from django.contrib import admin
from .models import Booking
from blog.models import Touch

# Register your models here.


admin.site.register(Booking)


class TouchAdmin(admin.ModelAdmin):
    model = Touch

    list_display = ["touch_name", "touch_email"]

admin.site.register(Touch, TouchAdmin)
