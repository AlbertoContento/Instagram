from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    user = models.ForeignKey(User, verbose_name="Usuario", on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField("Imagen", upload_to='posts_images/')
    caption = models.TextField("Comentario", max_length=500, blank=True)
    created_at = models.DateTimeField("Fecha de Creacion", auto_now_add=True)
    #ESte campo es para saber que usuarios le dan a me gusta a este post
    likes = models.ManyToManyField(User, verbose_name="Me gusta", related_name='liked_posts', blank=True)
    
    class Meta:#Para decir como quiero que me aparezca en el Admin
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def __str__(self):
        return f"{self.user.username} - {self.created_at}"
    

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, verbose_name="Usuario", on_delete=models.CASCADE, related_name='comments')
    text = models.TextField("Contenido del comentario", max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Comentario'
        verbose_name_plural = 'Comentarios'
        ordering = ['created_at']#para ordenarlo por fecha de creacion

    def __str__(self):
        return f"Coméntó {self.user.username} el post {self.post}"