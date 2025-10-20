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
from .forms import PostCreateForm, CommentCreateForm
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse
from django.http import JsonResponse
from django.db.models import Q
from posts.models import Comment

@method_decorator(login_required, name='dispatch')
class PostCreateView(CreateView):
    template_name = "posts/post_create.html"
    model = Post
    form_class = PostCreateForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.user = self.request.user
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
        context['comments'] = post.comments.all().order_by('created_at')
        return context

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


@login_required
def like_post_ajax(request, pk):
    if request.method == "POST":
        post = get_object_or_404(Post, pk=pk)

        if request.user in post.likes.all():
            post.likes.remove(request.user)
            liked = False
        else:
            post.likes.add(request.user)
            liked = True

        return JsonResponse({
            "success": True,
            "liked": liked,
            "nLikes": post.likes.count()
        })

    return JsonResponse({"success": False, "message": "Método no permitido."}, status=405)

@login_required
def buscar_amigos(request):
    query = request.GET.get('q', '')
    results = []

    if query:
        user_profile = request.user.profile
        seguidos = Follow.objects.filter(follower=user_profile).values_list('following', flat=True)
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
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse({"success": False}, status=403)
    return redirect(request.META.get('HTTP_REFERER', '/'))


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
                    'success': True,
                    'username': comment.user.username,
                    'text': comment.text,
                    'profile_picture': profile_picture_url,
                    'can_delete': request.user == comment.user,
                    'comment_id': comment.id
                })

            return redirect(request.META.get('HTTP_REFERER', '/'))
    return JsonResponse({'success': False}, status=400)


@login_required
@require_POST
def responder_comentario(request, comment_id):
    parent_comment = get_object_or_404(Comment, pk=comment_id)
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
            'profile_picture': request.user.profile.profile_picture.url if request.user.profile.profile_picture else ''
        })
    return JsonResponse({'success': False}, status=400)
