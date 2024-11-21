from .models import Post, Comment
from django import forms


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'user',
            'image',
            'caption'
        ]

#Formulario de comentarios
class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'text',
        ]