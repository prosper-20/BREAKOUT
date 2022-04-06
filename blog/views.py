from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post

class Home(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = "blog/news.html"


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/news_detail.html"

