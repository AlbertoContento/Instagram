from django.contrib import admin
from django.urls import path
from debug_toolbar.toolbar import debug_toolbar_urls # type: ignore
#importamos las vistas
from .views import HomeView, LoginView, RegisterView, ContactView, LegalView, logout_view, ProfileDetailView, ProfileUpdateView, ProfileListView
#importamos esto para que podamos ver las imagenes staticas
from django.conf.urls.static import static
from django.conf import settings
from posts.views import PostCreateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('profile/list/', ProfileListView.as_view(), name='profile_list'),
    path('profile/<pk>/', ProfileDetailView.as_view(), name='profile_detail'),
    path('profile/update/<pk>/', ProfileUpdateView.as_view(), name='profile_update'),
    path('posts/create/', PostCreateView.as_view(), name='post_create'),
    path('legal/', LegalView.as_view(), name='legal'),
    path('logout/', logout_view, name='logout')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
