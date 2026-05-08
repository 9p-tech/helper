from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('django-admin/', admin.site.urls),

    path('api/auth/', include('apps.accounts.urls')),
    path('api/', include('apps.catalog.urls')),
    path('api/', include('apps.cart.urls')),
    path('api/', include('apps.orders.urls')),
    path('api/whatsapp/', include('apps.whatsapp_bot.urls')),
    path('api/admin/', include('apps.claims.urls')),

    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
