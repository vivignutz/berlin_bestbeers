from . import views
from django.urls import path, include
from .views import HomeView, Blog, AddPost, BarsList, Rating, PostLike, PostLike, PostDetail, PostUpdate, PostDelete, CommentUpdate, CommentDelete


urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('blog/', Blog.as_view(), name='blog'),
    path('add_post/', AddPost.as_view(), name='add_post'),
    path('bars_list/', BarsList, name='bars_list'),
    #    path('review/<int:pk>/', ReviewView.as_view(), name='review'),
    path('post_detail/<slug:slug>/', PostDetail.as_view(), name='post_detail'),
    path('like/<slug:slug>/', PostLike.as_view(), name='post_like'),
    path('update_post/edit/<slug:slug>/',
         PostUpdate.as_view(), name='update_post'),
    path('delete/<slug:slug>/remove', PostDelete.as_view(), name='delete_post'),
    path('<slug:slug>/update_comment/<int:pk>',
         CommentUpdate.as_view(), name='update_comment'),
    path('<slug:slug>/delete_comment/<int:pk>',
         CommentDelete.as_view(), name='delete_comment'),
    path('bar/<int:bar_id>/rating/', views.rating, name='rating'),
]
