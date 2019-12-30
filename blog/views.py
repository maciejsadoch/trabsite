from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from django.views.generic.base import View
from .models import Post, Comment
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


class PostDetailView(View):

    def get(self, request, year, month, day, post):
        post = get_object_or_404(Post, status='published',
                                 publish__year=year, publish__month=month,
                                 publish__day=day, slug=post)
        comments = post.comments.filter(active=True)
        comment_form = CommentForm()
        new_comment = None
        ctx = {
            'post': post,
            'comments': comments,
            'new_comment': new_comment,
            'comment_form': comment_form,
        }
        return render(request, 'blog/post/detail.html', ctx)

    def post(self, request, year, month, day, post):
        post = get_object_or_404(Post, status='published',
                                 publish__year=year, publish__month=month,
                                 publish__day=day, slug=post)
        comments = post.comments.filter(active=True)
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            ctx = {
                'post': post,
                'comment_form': comment_form,
                'comments': comments,
                'new_comment': new_comment,
            }
        return render(request, 'blog/post/detail.html', ctx)

class SharePostView (View):

    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id, status='published')
        sent = False
        ctx = {
            'post': post,
            'form': EmailPostForm(),
        }
        return render(request, 'blog/post/share.html', ctx)

    def post(self, request, post_id):
        email_form = EmailPostForm(request.POST)
        post = get_object_or_404(Post, id=post_id, status='published')
        if email_form.is_valid():
            data = form.cleaned_data
            post_url = request.post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{data['name']} ({data['email']}) recommends you reading {post.title}"
            message = f"Read {post.title} at {post_url}\n\n{data['name']}\'s comments: {data['comments']}"
            send_mail(subject, message, 'admin@myblog.com', [data['to']])
            sent = True
            ctx = {
                'post': post,
                'form': email_form,
                'sent': sent,
            }
        return render(request, 'blog/post/share.html', ctx)



