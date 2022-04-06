from django.urls import path
from .views import Home, PostDetailView

urlpatterns = [
    path("", Home.as_view(), name="blog_home"),
    path('<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    
]