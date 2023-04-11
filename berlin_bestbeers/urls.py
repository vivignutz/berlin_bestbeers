from . import views
from django.urls import path, include
from .views import HomeView, BarList, Review, AddPost, PostLike, PostDetail, PostUpdate, PostDelete, CommentUpdate, CommentDelete
from django.views.generic import ListView

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('barlist/', BarList.as_view(), name='barlist'),
    path('add_post/', AddPost.as_view(), name='add_post'),
    path('review/<int:pk>/', Review.as_view(), name='review'),
    path('post_detail/<slug:slug>/', PostDetail.as_view(), name='post_detail'),
    path('like/<slug:slug>/', PostLike.as_view(), name='post_like'),
    path('update_post/edit/<slug:slug>/',
         PostUpdate.as_view(), name='update_post'),
    path('delete/<slug:slug>/remove', PostDelete.as_view(), name='delete_post'),
    path('<slug:slug>/update_comment/<int:pk>',
         CommentUpdate.as_view(), name='update_comment'),
    path('<slug:slug>/delete_comment/<int:pk>',
         CommentDelete.as_view(), name='delete_comment'),
]
