from django.urls import path, include
from .views import HomeView, RoomDetailView, contact, about, contact_us, search_rooms, news, TestView, staff, rooms
# tester
from . import views

urlpatterns = [
    path("", HomeView, name="home"),
    # path("", HomeView.as_view(), name="home"),
    # path('room/<slug:slug>/', views.detail_view, name='detail'),
    path("contact/", views.contact, name="contact"),
    path("about/", views.about, name="about"),
    path('search/', views.search_rooms, name="search_rooms"),
    path('news/', views.news, name="news"),
    # path("booker/<slug:slug>/", views.tester, name="tester"),
    path("gallery/", views.gallery, name="gallery"),
    path('staff/', views.staff, name="staff"),
    path('rooms/', views.rooms, name="rooms"),
    path('tester/<category>', TestView.as_view(), name="test_booking"),
    path('contact-us/', contact_us, name='contact_us')

]
 