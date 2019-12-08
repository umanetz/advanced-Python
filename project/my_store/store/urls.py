from django.conf.urls import url
from . import views
from django.conf.urls import handler404
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    # url(r'^$', views.main, name='main'),
    url(r'^catalog/$', views.catalog, name='catalog'),
    # url(r'^contact$', views.contact, name='contact'),
    # url(r'^catalog/[a-z]+/$', views.catalog_category, name="catalog category"),
    # url(r'^sales$', views.sales, name="sales"),
    # url(r'^products/[^/]+/$', views.item, name="item"),
    # url(r'^cart/', views.cart, name='cart'),
    # url(r'^add-to-cart/$', views.add, name='add'),
    # url(r'^remove-from-cart/$', views.remove, name='remove'),
    # url(r'^cart-total-price/$', views.get_total_price, name='cart total price'),
    # url(r'^success', views.success, name='success')

]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)