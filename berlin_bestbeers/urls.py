from . import views
from django.urls import path, include
from .views import HomeView, BarList, AddPost, PostLike, PostDetail, PostUpdate, PostDelete, CommentUpdate, CommentDelete


urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('barlist/', BarList.as_view(), name='barlist'),
    path('add_post/', AddPost.as_view(), name='add_post'),
    path('bars/', BarListView.as_view(), name='bars_list'),
    path('review/<int:pk>/', ReviewCreateView.as_view(), name='review_create'),
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
