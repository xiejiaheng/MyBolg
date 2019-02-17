"""untitled2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path,include
from article import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor',include('ckeditor_uploader.urls')),
    path('',views.index, name= 'index'),
    path('info/<int:id>', views.info, name='info'),
    path('type/<int:id>', views.blogs_type, name='blogs_type'),
    path('date/<int:year>/<int:month>', views.blogs_with_date, name='blogs_with_date'),
    path('search/', views.search, name='search'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('phone_code/',views.phone_code),
    path('about/', views.about, name='about'),
    path('erweima/', views.erweima, name='erweima'),
    path('tupian/', views.tupian, name='tupian'),

]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)