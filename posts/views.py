from django.views.generic.edit import CreateView
from posts.models import Post
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404, redirect


from profiles.models import Follow, UserProfile
from .forms import PostCreateForm, CommentCreateForm # type: ignore
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse
from django.db.models import Q
from posts.models import Comment



@method_decorator(login_required, name='dispatch')#protege las vistas de usuarios que no esten autenticados
class PostCreateView(CreateView):
    template_name = "posts/post_create.html"
    model = Post
    form_class = PostCreateForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.user = self.request.user  # Asignar usuario actual
        response = super().form_valid(form)
        messages.success(self.request, "Publicación creada correctamente.")
        return response


class PostDetailView(DetailView, CreateView):
    template_name = "posts/post_detail.html"
    model = Post
    context_object_name = "post"
    form_class = CommentCreateForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.post = self.get_object()
        return super(PostDetailView, self).form_valid(form)
    
    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, "Comentario añadido correctamente.")
        return reverse('post_detail', args=[self.get_object().pk])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context['profile'] = post.user.profile
        context['comments'] = post.comments.all().order_by('created_at')  # <-- añade los comentarios aquí
        return context

#Vista basada en una funcion con el decorador login required
@login_required
def like_post(request, pk):
    post = Post.objects.get(pk=pk)
    if request.user in post.likes.all():
        messages.add_message(request, messages.ERROR, "Ya no te gusta está publicacion")
        post.likes.remove(request.user)
    else:
        messages.add_message(request, messages.SUCCESS, "Te gusta esta publicacion")
        post.likes.add(request.user)

    return HttpResponseRedirect(reverse('post_detail', args=[pk]))


#Misma vista que la anterior pero con AJAX(javascript)
@login_required
def like_post_ajax(request, pk):
    post = Post.objects.get(pk=pk)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        return JsonResponse(
            {
                'message': 'Ya no te gusta esta publicacion',
                'liked': False,
                'nLikes': post.likes.all().count()
            }
        )
    else:
        post.likes.add(request.user)
        return JsonResponse(
            {
                'message': 'Te gusta esta publicacion',
                'liked': True,
                'nLikes': post.likes.all().count()
            }
        )
    

#BUSQUEDA AMIGOS
@login_required
def buscar_amigos(request):
    query = request.GET.get('q', '')
    results = []

    if query:
        user_profile = request.user.profile

        # Obtenemos todos los perfiles a los que el usuario sigue
        seguidos = Follow.objects.filter(follower=user_profile).values_list('following', flat=True)

        # Filtramos los perfiles seguidos que coincidan con la búsqueda
        perfiles_encontrados = UserProfile.objects.filter(
            id__in=seguidos
        ).filter(
            Q(user__username__icontains=query) | Q(user__first_name__icontains=query)
        )

        for perfil in perfiles_encontrados:
            results.append({
                'pk': perfil.user.pk,
                'username': perfil.user.username,
                'nombre': perfil.user.first_name,
                'foto': perfil.profile_picture.url if perfil.profile_picture else '/static/icons/mi_perfil.png'
            })

    return JsonResponse({'resultados': results})


#ELIMINAR COMENTARIOS
@login_required
def eliminar_comentario(request, pk):
    comentario = get_object_or_404(Comment, pk=pk)
    if request.method == "POST":
        if request.user == comentario.user:
            comentario.delete()
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse({"success": True})
            else:
                return redirect(request.META.get('HTTP_REFERER', '/'))
    # Si no autorizado
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse({"success": False}, status=403)
    return redirect(request.META.get('HTTP_REFERER', '/'))


# CREAR COMENTARIOS (con AJAX)
@login_required
def crear_comentario(request, post_id):
    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            post = get_object_or_404(Post, id=post_id)
            comment = Comment.objects.create(post=post, user=request.user, text=text)

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                profile_picture_url = ''
                if hasattr(comment.user, 'profile') and comment.user.profile.profile_picture:
                    profile_picture_url = comment.user.profile.profile_picture.url

                return JsonResponse({
                    'success': True,  # ✅ Necesario para que el JS funcione
                    'username': comment.user.username,
                    'text': comment.text,
                    'profile_picture': profile_picture_url,
                    'can_delete': request.user == comment.user,
                    'comment_id': comment.id
                })

            return redirect(request.META.get('HTTP_REFERER', '/'))
        

#RESPONDER COMENTARIO
@login_required
@require_POST
def responder_comentario(request, comment_id):
    parent_comment = get_object_or_404(Comment, pk=comment_id)
    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            new_comment = Comment.objects.create(
                user=request.user,
                post=parent_comment.post,
                text=text,
                parent=parent_comment
            )
            return JsonResponse({
                'success': True,
                'comment_id': new_comment.id,
                'text': new_comment.text,
                'username': request.user.username,
                'profile_picture': request.user.profile.profile_picture.url if request.user.profile.profile_picture else '',
                'can_delete': True
            })
    return JsonResponse({'success': False}, status=400)