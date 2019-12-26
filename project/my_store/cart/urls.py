from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views


# Cart Urls
urlpatterns = [
    path('cart/', views.cart_detail, name='cart-detail'),
    path('cart/<int:pk_item>/add/', views.cart_add, name='cart-add'),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)