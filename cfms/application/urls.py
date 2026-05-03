"""
URL configuration for application project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import include, path
from django.contrib.auth import views as auth_views

urlpatterns = [
    # path('', CustomLoginView.as_view(), name='login'),
    path('admin/', admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    # slight problem ; I mistakeningly set the app to be dashboard and it would take too long to refadctor
    # so pretend this is just complaint
    path('', include('dashboard.urls')),
    # summary is the actual dashboard
    path('', include('summary.urls')),
]
