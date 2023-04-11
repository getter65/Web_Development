from django.urls import path
from blog.apps import BlogConfig
from blog.views import PostListView, PostDetailView
from django.views.decorators.cache import cache_page

app_name = BlogConfig.name

urlpatterns = [
    path('posts/', cache_page(60)(PostListView.as_view()), name='post_list'),
    path('posts/<int:pk>', PostDetailView.as_view(), name='post_detail'),
    ]