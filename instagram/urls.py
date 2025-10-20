from django.contrib import admin
from django.urls import path
from debug_toolbar.toolbar import debug_toolbar_urls # type: ignore
#importamos las vistas
from .views import HomeView, LoginView, RegisterView, ContactView, LegalView, logout_view, ProfileDetailView, ProfileUpdateView, ProfileListView
#importamos esto para que podamos ver las imagenes staticas
from django.conf.urls.static import static
from django.conf import settings
from posts.views import PostCreateView, PostDetailView, like_post, like_post_ajax, buscar_amigos, eliminar_comentario, crear_comentario, responder_comentario
from . import views


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
    path('posts/<pk>/', PostDetailView.as_view(), name='post_detail'),
    path('posts/like/<pk>/', like_post, name='post_like'),
    path('posts/like-ajax/<pk>/', like_post_ajax, name='post_like_ajax'),
    path('legal/', LegalView.as_view(), name='legal'),
    path('logout/', logout_view, name='logout'),
    path('buscar-amigos/', buscar_amigos, name='buscar_amigos'),
    path('comentario/eliminar/<int:pk>/', eliminar_comentario, name='eliminar_comentario'),
    path('comentario/nuevo/<int:post_id>/', crear_comentario, name='crear_comentario'),
    path('comentario/<int:comment_id>/responder/', responder_comentario, name='responder_comentario'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)