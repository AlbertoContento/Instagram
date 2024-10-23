from django.contrib import admin
from django.urls import path
from debug_toolbar.toolbar import debug_toolbar_urls # type: ignore

urlpatterns = [
    path('admin/', admin.site.urls),
]
