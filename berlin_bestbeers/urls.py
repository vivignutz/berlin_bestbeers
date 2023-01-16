from django.urls import path
from . import views



urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('like/<slug:slug>/', views.PostLike.as_view(), name='post_like'),
    path('add/,slug:slug>', views.PostAdd.as_view(), name='post_add'),
    path('post/<slug:slug>/', views.PostDetail.as_view(), name='blog_post'),
#    path('<slug:slug>/update/', views.PostUpdate.as_view(), name='post_update'),
#    path('<slug:slug>/delete/', views.PostDelete.as_view(), name='post_delete'),
#    path('<slug:slug>/comment-update/<int:pk>', views.CommentUpdate.as_view(), name='comment_update'),
]