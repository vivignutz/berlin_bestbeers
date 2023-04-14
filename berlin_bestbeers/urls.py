from . import views
from django.urls import path, include
from django.views.generic import ListView
from .views import HomeView, BlogView, BarsList, AddPost, PostLike, PostLike, PostDetail, PostUpdate, PostDelete, CommentUpdate, CommentDelete


urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('blog/', BlogView.as_view(), name='blog'),
    path('add_post/', AddPost.as_view(), name='add_post'),
    path('bars_list/', BarsList.as_view(), name='bars_list'),
    path('post_detail/<slug:slug>/', PostDetail.as_view(), name='post_detail'),
    path('like/<slug:slug>/', PostLike.as_view(), name='post_like'),
    path('update_post/edit/<slug:slug>/',
         PostUpdate.as_view(), name='update_post'),
    path('delete/<slug:slug>/remove', PostDelete.as_view(), name='delete_post'),
    path('<slug:slug>/update_comment/<int:pk>',
         CommentUpdate.as_view(), name='update_comment'),
    path('<slug:slug>/delete_comment/<int:pk>',
         CommentDelete.as_view(), name='delete_comment'),
    # path('post/<int:post_id>/rating/', RatingView.as_view(), name='rating'),
]
