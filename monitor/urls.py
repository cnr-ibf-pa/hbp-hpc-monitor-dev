"""monitor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path
from monitor import views


urlpatterns = [
 
    path('', views.index, name='index'),

    path('user', views.get_user, name='user'),
    path('status', views.get_status, name='status'),
    
    path('pizdaint', views.get_hpc_info, name='pizdaint'),
    path('pizdaint/projects', views.get_hpc_info, name='pizdaint-projects'),
    path('pizdaint/check', views.check_job_submission, name='pizdaint-check-job-submission'),
    path('marconi', views.get_hpc_info, name='marconi'),
    path('marconi/projects', views.get_hpc_info, name='marconi-projects'),
    path('marconi/check', views.check_job_submission, name='marconi-check-job-submission')

]
