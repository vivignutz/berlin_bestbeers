from . import views
from django.urls import path, include
from .views import HomeView, BarList, AddPost, PostLike, PostDetail, PostUpdate


urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('barlist/', BarList.as_view(), name='barlist'),
    path('add_post/', AddPost.as_view(), name='add_post'),
    path('post_detail/<slug:slug>/', PostDetail.as_view(), name='post_detail'),
    path('like/<slug:slug>/', PostLike.as_view(), name='post_like'),
    path('update_post/<slug:slug>/', views.PostUpdate.as_view(), name='update_post'),
#    path('<slug:slug>/delete/', views.PostDelete.as_view(), name='post_delete'),
#    path('<slug:slug>/comment-update/<int:pk>', views.CommentUpdate.as_view(), name='comment_update'),
#    path('ModelForm/', views.forms_ModelForm(), name='form_Modelform'),
]