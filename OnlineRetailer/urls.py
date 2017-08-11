"""OnlineRetailer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns, static

from .modules.products import views as product_views
from .modules.experiments import views as exp_views

urlpatterns = [
    url(r'^admin/',
        admin.site.urls),

    url(r'^$',
        product_views.product_list_view, name='product_list'),
    url(r'^(?P<page>[0-9]+)$',
        product_views.product_list_view, name='product_list_page'),
    url(r'^cart$',
        product_views.product_cart_view, name='cart'),
    url(r'^checkout$',
        product_views.product_confirmation_view, name='confirm'),

    url(r'^add/(?P<item_id>[0-9]+)$',
        product_views.add_to_cart, name='add_to_cart'),
    url(r'^remove/(?P<item_id>[0-9]+)$',
        product_views.remove_from_cart, name='remove_from_cart'),
    url(r'^control/$',
        exp_views.exp_control_view, name='control'),
    url(r'^control/random$',
        exp_views.random, name='random'),
    url(r'^control/delete$',
        exp_views.delete, name='delete')
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
