from django.urls import path, include, path
from . import views
from .views import PostList, PostDetail, PostAdd, BarsList


urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('berlin_bestbeers/', views.BarsList.as_view()),
    path('barslist/', views.BarsList.as_view()),
    path('add_post/', views.PostAdd.as_view(), name='add_post'),
    path('post_detail/<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('like/<slug:slug>/', views.PostLike.as_view(), name='post_like'),
#    path('<slug:slug>/update/', views.PostUpdate.as_view(), name='post_update'),
#    path('<slug:slug>/delete/', views.PostDelete.as_view(), name='post_delete'),
#    path('<slug:slug>/comment-update/<int:pk>', views.CommentUpdate.as_view(), name='comment_update'),
#    path('ModelForm/', views.forms_ModelForm(), name='form_Modelform'),
]