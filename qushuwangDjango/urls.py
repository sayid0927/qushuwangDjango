"""qushuwangDjango URL Configuration

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
from App.views import *

urlpatterns = [

    url(r'^admin/', admin.site.urls),
    url(r'^book_list', book_list),
    url(r'^book_name', book_name),
    url(r'^book_dir', book_dir),
    url(r'^book_content', book_content),
    url(r'^apk_update', apk_update),
    url(r'^apk_path', apk_update_path),
    url(r'^manhun_list', manhun_list),
    url(r'^manhun_name_list', manhun_name_list),



]
