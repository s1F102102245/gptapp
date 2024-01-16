"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path,  include
import gptapp.views
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage



'''
urlpatterns = [
    path('admin/', admin.site.urls),
    path('top/', gptapp.views.root),
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('favicon.ico'))),
]   + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
'''

urlpatterns = [
    path('admin/', admin.site.urls),
    path('top/', gptapp.views.root),
    path('gptapp/pattern/<username>/', gptapp.views.pattern, name='pattern'),
    path('gptapp/param/', gptapp.views.param, name='param'),
    path('gptapp/', gptapp.views.index, name="index"),
    path('chat/', gptapp.views.chat_view, name='chat_view'),
    #path('', gptapp.views.ocr_view, name='ocr_view'),
    path('', gptapp.views.math_Answerer, name='math_Answerer'),
]   + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
  