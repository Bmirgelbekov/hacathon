from django.db import models
from django.contrib.auth import get_user_model

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

    address = models.CharField(max_length=200)
    rooms = models.CharField(max_length=10, choices=ROOMS_COUNT, default='NOT')
    

    class Meta:
        verbose_name = 'Квартира'
        verbose_name_plural = 'Квартиры'
        ordering = ['created_at']

    def __str__(self) -> str:
        return self.title


