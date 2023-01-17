from django.urls import path, include
from . import views, post_detail


urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('berlin_bestbeers/', views.PostList.as_view(), name='berlin_bestbeers'),
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('like/<slug:slug>/', views.PostLike.as_view(), name='post_like'),
    path('post_add/', views.PostAdd.as_view(), name='post_add'),
#    path('<slug:slug>/update/', views.PostUpdate.as_view(), name='post_update'),
#    path('<slug:slug>/delete/', views.PostDelete.as_view(), name='post_delete'),
#    path('<slug:slug>/comment-update/<int:pk>', views.CommentUpdate.as_view(), name='comment_update'),
]