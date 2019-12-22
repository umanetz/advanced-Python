from django.conf.urls import url
from . import views
from django.conf.urls import handler404
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings
from .views import Catalog, CategoryList, ItemDetail, RegisterView, LoginView
from django.contrib.auth import views as auth_views



urlpatterns = [
    # url(r'^$', views.main, name='main'),
    url(r'^catalog/$', Catalog.as_view(), name='catalog'),
    url(r'^catalog/(?P<category_name>[a-z]+)/$', CategoryList.as_view(), name="catalog category"),
    url(r'^product/(?P<category_name>[a-z]+)/(?P<pk>\d+)/$', ItemDetail.as_view(), name="item-detail"),
    url(r'^register/$', RegisterView.as_view(), name="user-register"),
    url(r'^login/$', LoginView.as_view(), name="user-login"),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='user-logout'),
]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)