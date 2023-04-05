from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import Appartment #, Comment
from .serializers import AppartmentSerializer, AppartmentListSerializer #, CommentSerializer
from .permissions import IsAuthor

class AppartmentViewSet(ModelViewSet):
    queryset = Appartment.objects.all()
    serializer_class = AppartmentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['rooms']

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