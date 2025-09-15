from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from kids.views import home
from users.views import my_bookings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('', home, name='home'),
    # ...removed movies app URL include...
    # ...removed languageleague URL includes...
    path('kids/', include('kids.urls')),
    path('my-bookings/', my_bookings, name='my_bookings'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
