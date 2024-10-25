from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, verbose_name= "Usuario", on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField('Imagen de perfil', upload_to='profile_pictures/', blank=True, null=True)
    bio = models.TextField('Biografía', max_length=500, blank=True)
    birth_date = models.DateField('Fecha de nacimiento', null=True, blank=True)
    #Este campo dice que no es simetrico(si un user sigue a otro el otro no tiene porque seguirle), through es para ver si queremos tener un campo intermedio para saber quien sigue a quien y desde cuando
    followers = models.ManyToManyField("self", symmetrical=False, related_name='following', through='Follow')

    class Meta:#Para decir como quiero que me aparezca en el Admin
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'

    def __str__(self):
        return self.user.username
    
#Creamos el modelo de follow para poder ver desde cuando sigue a alguien y a quien sigue y quien le sigue
class Follow(models.Model):
    follower = models.ForeignKey(UserProfile, verbose_name='¿Quien sigue?', on_delete=models.CASCADE, related_name='follower_set')
    following = models.ForeignKey(UserProfile, verbose_name='¿A quien sigue?', on_delete=models.CASCADE, related_name='following_set')
    #para poder guardar en que fecha comenzo el seguimiento
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='¿Desde cuando lo sigue?')

#Con esto le decimos que un user no puede seguir al mismo tipo de perfil mas de una vez
    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return f"{self.follower} follows {self.following}"
    
    class Meta:
        verbose_name = 'Seguidor'
        verbose_name_plural = 'Seguidores'