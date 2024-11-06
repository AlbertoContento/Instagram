from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.views.generic import TemplateView, CreateView, DetailView, ListView
from .forms import RegistrationForm, LoginForm
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import HttpResponseRedirect
from django.views.generic.edit import FormView, UpdateView
from profiles.models import UserProfile
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from posts.models import Post


#Vamos a mostrar en la home las ultimas publicaciones
class HomeView(TemplateView):
    template_name = "general/home.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
#guardamos en last_posts los ultimos 5 posts
        last_posts = Post.objects.all().order_by('-created_at')[:5]
        context['last_posts'] = last_posts

        return context


#FORMVIEW: vista para formulario
class LoginView(FormView):
    template_name = "general/login.html"
    form_class = LoginForm

    def form_valid(self, form):#Fomulario es valido
        usuario = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=usuario, password=password)#Guardamos usuario y contraseña si el usuario existe en nuestra BD
        if user is not None:#Si el user no es None
            login(self.request, user)#Logueamos al usuario
            messages.add_message(self.request, messages.SUCCESS, f'Bienvenido de nuevo {user.username}')
            return HttpResponseRedirect(reverse('home'))#una vez logueado le redirigimos a la home
        else:#si el usuario es None, mandamos mensaje de error
            messages.add_message(
                self.request, messages.ERROR, 'Usuario no válido o contraseña no válida')
            return super(LoginView, self).form_invalid(form)#Devolvemos que el login es invalido


#CREATEVIEW: para poder registrar usuarios
class RegisterView(CreateView):
    model = User
    template_name = "general/register.html"
    success_url = reverse_lazy('login')#Pagina que mostrar despues de registrar
    form_class = RegistrationForm#le pasamos el formulario

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, "Usuario creado correctamente.")
        return super(RegisterView, self).form_valid(form)


class LegalView(TemplateView):
    template_name = "general/legal.html"


class ContactView(TemplateView):
    template_name = "general/contact.html"


#FUNCION PARA CERRAR SESION
@login_required#protege las vistas de usuarios que no esten autenticados
def logout_view(request):
    logout(request)
    messages.add_message(request, messages.INFO, "Se ha cerrado sesión correctamente.")
    return HttpResponseRedirect(reverse('home'))


#DETAILVIEW
@method_decorator(login_required, name='dispatch')#protege las vistas de usuarios que no esten autenticados
class ProfileDetailView(DetailView):
    model = UserProfile
    template_name = "general/profile_detail.html"
    context_object_name = "profile"#con esto vamos a poder hacer referencia a todos los campos 

#DETAILVIEW
@method_decorator(login_required, name='dispatch')#protege las vistas de usuarios que no esten autenticados
class ProfileListView(ListView):
    model = UserProfile
    template_name = "general/profile_list.html"
    context_object_name = "profiles"#con esto vamos a poder hacer referencia a todos los campos 
#Con esto excluimos que nos salga nuestro propio perfil
    def get_queryset(self):
        return UserProfile.objects.all().exclude(user=self.request.user)
    

#UPDATEVIEW
@method_decorator(login_required, name='dispatch')#protege las vistas de usuarios que no esten autenticados
class ProfileUpdateView(UpdateView):
    model = UserProfile
    template_name = "general/profile_update.html"
    context_object_name = "profile"
    fields = ['profile_picture', 'bio', 'birth_date']
    
    #Esto es para comprobar si estamos editando nuestro perfil o el de otra persona y si es asi le mandamos a la home
    def dispatch(self, request, *args, **kwargs):
        user_profile = self.get_object()
        if user_profile.user != self.request.user:
            return HttpResponseRedirect(reverse('home'))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):#Cuando este validado mande mensaje
        messages.add_message(self.request, messages.SUCCESS, "Perfil editado correctamente.")
        return super(ProfileUpdateView, self).form_valid(form)
    
    def get_success_url(self):#devuelve la url del perfil editado
        return reverse('profile_detail', args=[self.object.pk])