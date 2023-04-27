from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from sneakers.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('captcha/', include('captcha.urls')),
    path('', include('sneakers.urls')),
    path('api/v1/sneaker/', SneakerAPIList.as_view()),
    path('api/v1/sneaker/<int:pk>/', SneakerAPIUpdate.as_view()),
    path('api/v1/sneakerdelete/<int:pk>/', SneakerAPIDestroy.as_view()),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = pageNotFound
handler403 = pageForbidden
handler400 = pageBadRequest
