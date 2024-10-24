from django.contrib import admin
from django.urls import path
from debug_toolbar.toolbar import debug_toolbar_urls # type: ignore
#importamos las vistas
from .views import HomeView, LoginView, RegisterView, ContactView, LegalView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('legal/', LegalView.as_view(), name='legal')
]
