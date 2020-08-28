"""iproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from blog import views as blog_view
from django.views.static import serve
from .settings import MEDIA_ROOT, STATIC_ROOT
# serve and MEDIA_ROOT is very important for media file,so we need to import them

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', blog_view.index),
    path('index/', blog_view.index),
    path('single/post/', blog_view.single),
    path('single/post/<int:post_id>/', blog_view.single),
    path('archive/', blog_view.archive),
    path('contact/', blog_view.contact),
    path('wechat/', blog_view.wechat),
    path('contact/receive/', blog_view.contact_rec_email),
    path('media/<path:path>', serve, {'document_root': MEDIA_ROOT}),
    path('static/<path:path>', serve, {'document_root': STATIC_ROOT}),
    path('comment/', blog_view.comment),
    path('search/', blog_view.search),
    path('comment/post/', blog_view.comment_post),
    path('subscribe/', blog_view.subscribe)
]
