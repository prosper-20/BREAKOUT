from django.urls import path
from .views import Home, PostDetailView, PostCreateView

urlpatterns = [
    path("", Home.as_view(), name="blog_home"),
    path("<int:pk>/", PostDetailView.as_view(), name='post-detail'),
    path("create/", PostCreateView.as_view(), name="post_create")
    
]