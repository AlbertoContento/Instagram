from django.views.generic.edit import CreateView
from posts.models import Post
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.detail import DetailView
from .forms import PostCreateForm, CommentCreateForm # type: ignore
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse


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