from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status

from .models import Appartment, Comment
from .serializers import AppartmentSerializer, AppartmentListSerializer, CommentSerializer
from .permissions import IsAuthor

from rest_framework.decorators import action
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
    
    def get_serializer_class(self):
        if self.action == 'comment':
            return CommentSerializer
        return super().get_serializer_class()
    
    @action(methods=['POST'], detail=True)
    def comment(self, request, pk=None):
        appartment = self.get_object()
        if request.method == 'POST':
            serializer = CommentSerializer(data=request.data, context={
                'request': request}
                )
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.user, appartment=appartment)
            return Response({'message': f'Создан коммент {serializer.data}'})
        return Response({'error': 'oops'})


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'destroy']:
            self.permission_classes = [IsAuthor]
        return super().get_permissions()
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context

