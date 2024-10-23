from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField('Imagen de perfil', upload_to='profile_pictures/', blank=True, null=True)
    bio = models.TextField('Biografía', max_length=500, blank=True)
    birth_date = models.DateField('Fecha de nacimiento', null=True, blank=True)
    #followers = models.ManyToManyField("self", symmetrical=False, related_name='following', through='Follow')

    class Meta:#Para decir como quiero que me aparezca en el Admin
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'

    def __str__(self):
        return self.username