from django.urls import path
from .views import PostListView, PostDetailView, SharePostView

app_name = 'blog'

urlpatterns = [
    # post views
    path('', PostListView.as_view(), name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', PostDetailView.as_view(), name='post_detail'),
    path('<int:post_id>/share/', SharePostView.as_view(), name='share_post')
]