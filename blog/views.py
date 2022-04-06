from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from .models import Post

class Home(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = "blog/news.html"


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/news_detail.html"


class PostCreateView(CreateView):
    model = Post

    fields = ["title", "content", "category", "image"]


    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

