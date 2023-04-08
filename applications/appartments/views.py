from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import Appartment #, Comment
from .serializers import AppartmentSerializer, AppartmentListSerializer#, CommentSerializer
from .permissions import IsAuthor

from django.views.decorators.cache import  cache_page
from django.utils.decorators import method_decorator


class AppartmentViewSet(ModelViewSet):
    queryset = Appartment.objects.all()
    serializer_class = AppartmentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['rooms']

    @method_decorator(cache_page(60))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @method_decorator(cache_page(60))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context
    
    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [IsAuthenticated]
        elif self.request.method in ['PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [IsAuthor]
        return super().get_permissions()
    

# ПРОБНАЯ ВЬЮШКА
# class CommentViewSet(ModelViewSet):
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer

#     def get_permissions(self):
#         if self.action == 'create':
#             self.permission_classes = [IsAuthenticated]
#         elif self.action in ['update', 'destroy']:
#             self.permission_classes = [IsAuthor]
#         return super().get_permissions()
    
#     def get_serializer_context(self):
#         context = super().get_serializer_context()
#         context.update({'request': self.request})
#         return context