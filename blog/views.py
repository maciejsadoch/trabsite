from django.shortcuts import render, get_object_or_404
from django.views.generic.base import View
from .models import Post
from django.views.generic import ListView


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


class PostDetailView(View):
    def get(self, request, year, month, day, post):
        post = Post.published.get(publish__year=year, publish__month=month, publish__day=day, slug=post)
        return render(request, 'blog/post/detail.html', {'post': post})