from django.urls import path
from .views import Home, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, PostCommentView, LikeView
from . import views

urlpatterns = [
    path("", Home.as_view(), name="blog_home"),
    path("create/", PostCreateView.as_view(), name="post_create"),
    path("<int:pk>/", PostDetailView.as_view(), name='post-detail'),
    path('<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path("<int:pk>/comment/", PostCommentView.as_view(), name="post_comment"),
    path("like/<int:pk>", views.LikeView, name='like_post'),
    path('travel/', views.travel_view, name="travel")
    
]