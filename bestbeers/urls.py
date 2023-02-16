from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('summernote/', include('django_summernote.urls')),
    path('', include('berlin_bestbeers.urls'), name='berlin_bestbeers-urls'),
    path('accounts/', include('allauth.urls')),
]

handler404 = 'berlin_bestbeers.views.handler404'
handler500 = 'berlin_bestbeers.views.handler500'
handler403 = 'berlin_bestbeers.views.handler403'
handler405 = 'berlin_bestbeers.views.handler405'
