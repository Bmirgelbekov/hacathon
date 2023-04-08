from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import Appartment,Favorites#, Comment
from .serializers import AppartmentSerializer, AppartmentListSerializer,FavoritesSerializer#, CommentSerializer
from .permissions import IsAuthor
from rest_framework.views import APIView
from rest_framework import viewsets

class AppartmentViewSet(ModelViewSet):
    queryset = Appartment.objects.all()
    serializer_class = AppartmentSerializer
    filter_backends = [filters.SearchFilter,DjangoFilterBackend]
    search_fields = ['title']
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
    
    

        # Создание избранного элемента
        favorite_item = FavoriteItem(user=user, item=item)
        favorite_item.save()

        # Возврат успешного ответа
        serializer = self.get_serializer(favorite_item)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    

class FavoritesViewSet(viewsets.ViewSet):
    serializer_class = FavoritesSerializer
    permission_classes = (AllowAny)

    def retrieve(self, request, pk=None):
        if request.user.is_authenticated:
            # Если пользователь авторизован, возвращаем его Favorites
            return Favorites.objects.get_or_create(user=request.user)[0]
        else:
            # Если пользователь неавторизован, возвращаем Favorites по умолчанию
            return Favorites.objects.get_or_create(user=None)[0]

    def update(self, request, pk=None):
        # Ваша логика обновления Favorites
        pass  



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