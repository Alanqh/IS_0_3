from django.urls import path
from blog import views

app_name = 'blog'


urlpatterns = [
    path('posts/lists', views.post_list, name='post_list'),
    path('posts/create/', views.create_post, name='create_post'),
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    path('posts/<int:post_id>/comment/', views.comment_post, name='comment_post'),
    path('posts/<int:post_id>/share/', views.share_post, name='share_post'),
    path('search/', views.search_posts, name='search_posts'),
    path('users/<int:user_id>/', views.user_profile, name='user_profile'),
    path('users/<int:user_id>/followers/', views.follower_list, name='follower_list'),
    path('users/<int:user_id>/following/', views.following_list, name='following_list'),
    path('posts/<int:post_id>/likes/', views.post_likes, name='post_likes'),
    path('posts/<int:post_id>/comments/', views.comments_list, name='comments_list'),
    path('like/<int:post_id>', views.like_post, name='like_post'),
    path('follow/<int:user_id>', views.follow_user, name='follow_user'),


]
