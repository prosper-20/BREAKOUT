from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Comment
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import CommentForm
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required


class Home(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = "blog/news.html"


@login_required
def LikeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    post.likes.add(request.user)
    return HttpResponseRedirect(reverse('post-detail', args=[str(pk)]))


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/news_detail.html"
    comments = Comment.objects.all()
    extra_context = {"comments": comments}

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data()
        stuff = get_object_or_404(Post, id=self.kwargs["pk"])
        total_likes = stuff.total_likes()
        context["total_likes"] = total_likes
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post

    fields = ["title", "content", "category", "image"]


    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostCommentView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    # success_url = "/"
    template_name = "blog/post_comment_form.html"

    def form_valid(self, form):
        form.instance.name = self.request.user
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.kwargs['pk']})


def travel_view(request):
    posts = Post.objects.filter(category=1).first()
    context = {
        "posts": posts,
    }
    return render(request, "blog/travel_detail.html", context)