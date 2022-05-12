from django.contrib import admin
from .models import Category, Room, RoomImage, Staff, HotelImage, Message, HomeBooking

admin.site.register(Category)
admin.site.register(Staff)
admin.site.register(HotelImage)

class MessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "message",)


admin.site.register(Message, MessageAdmin)




class RoomImageAdmin(admin.StackedInline):
    model = RoomImage



@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    inlines = [RoomImageAdmin]

    class Meta:
        model = Room

@admin.register(RoomImage)
class RoomImageAdmin(admin.ModelAdmin):
    pass


