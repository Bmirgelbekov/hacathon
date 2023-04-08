from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from rest_framework.exceptions import ValidationError

# Create your models here.
User = get_user_model()



class Appartment(models.Model):
    STATUS_CHOICES = (
        ('OPEN', 'Open'),
        ('CLOSED', 'Closed'),
    )
    ROOMS_COUNT = (
        ('NOT', 'Не указано'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('4+', '4+'),
    )

    title = models.CharField(max_length=150)
    price = models.PositiveIntegerField(verbose_name='цена')
    description = models.TextField()
    image = models.ImageField(upload_to='appartments', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    status = models.CharField(max_length=6, choices=STATUS_CHOICES, default='CLOSED')

    address = models.CharField(max_length=200, default='не указано')
    rooms = models.CharField(max_length=10, choices=ROOMS_COUNT, default='NOT')
    phone_number = models.CharField(max_length=10, validators=[RegexValidator(r'^\d+$', 'Введите только цифры')], blank=True)
    

    class Meta:
        verbose_name = 'Квартира'
        verbose_name_plural = 'Квартиры'
        ordering = ['created_at']

    def __str__(self) -> str:
        return self.title

class Favorites(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    posts = models.ManyToManyField(Appartment, blank=True)

    def clean(self):
        if self.posts.count() > settings.MAX_FAVORITES_POSTS:
            raise ValidationError('Favorites limit exceeded.')


#  ПРОБНЫЙ ВАРИАНТ КОММЕНТАРИЕВ 

# class Comment(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
#     text = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     sub_comment = models.ForeignKey(
#         'self', on_delete=models.CASCADE, null=True, blank=True
#     )
#     appartment = models.ForeignKey(
#         Appartment, on_delete=models.CASCADE, related_name='comments'
#     )

#     class Meta:
#         verbose_name = 'Комментарий'
#         verbose_name_plural = 'Комментарии'

#     def __str__(self) -> str:
#         return f'комментарий от {self.user.username}'

