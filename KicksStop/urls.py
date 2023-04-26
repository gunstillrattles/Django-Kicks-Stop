from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from sneakers.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('captcha/', include('captcha.urls')),
    path('', include('sneakers.urls')),
    path('api/v1/sneaker/', SneakerAPIList.as_view()),
    path('api/v1/sneaker/<int:pk>/', SneakerAPIUpdate.as_view()),
    path('api/v1/sneakerdelete/<int:pk>/', SneakerAPIDestroy.as_view()),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = pageNotFound
handler403 = pageForbidden
handler400 = pageBadRequest
