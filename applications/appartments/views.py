from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import filters
from django.db.utils import IntegrityError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import LimitOffsetPagination
from django.shortcuts import get_object_or_404
from rest_framework import status

from .models import Appartment, Favorites
from .serializers import AppartmentSerializer, AppartmentListSerializer, FavoritesSerializer
from .permissions import IsAuthor
from rest_framework.views import APIView
from rest_framework import viewsets, permissions

class AppartmentViewSet(ModelViewSet):
    queryset = Appartment.objects.all()
    serializer_class = AppartmentSerializer
    filter_backends = [filters.SearchFilter,DjangoFilterBackend]
    search_fields = ['title']
    filterset_fields = ['rooms']
    #реализация поиска 

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
    

class ApartamentsViewCreate(ModelViewSet):
    queryset = Appartment.objects.all()
    serializer_class = AppartmentSerializer
    filter_backends = [filters.SearchFilter,DjangoFilterBackend]
    search_fields = ['title']
    filterset_fields = ['rooms']
    
    def post(self, request, *args, **kwargs):
        serializer = Appartment(data=request.data)
        if serializer.is_valid():
            serializer.save(author=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FavoritesView(viewsets.ModelViewSet):
    queryset = Favorites.objects.all() # Update queryset to be a queryset
    serializer_class = FavoritesSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = [permissions.BasePermission]

    def post(self, request, *args, **kwargs):
        try:
            post_id = request.data.get('id')
            if post_id is not None:
            # Получение соответствующего экземпляра Post по post_id
                post = Appartment.objects.get(id=post_id)
            else:
                pass
        except IntegrityError as e:
            pass

            # Создание нового экземпляра Favorites с указанием значения post
            favorite = Favorites.objects.create(posts=post)
        post = get_object_or_404(Appartment, id=post_id)

        favorite = Favorites.objects.create(
            user=request.user,
            post=post
        )

        serializer = FavoritesSerializer(favorite)
        return Response(serializer.data)

    

    def get(self, request, *args, **kwargs):
        queryset = Favorites.objects.filter(user=request.user)
        paginated_queryset = self.paginate_queryset(queryset, request)
        serializer = FavoritesSerializer(paginated_queryset, many=True)
        return self.get_paginated_response(serializer.data)
    
    
# class FavoriteDeleteView(viewsets.ModelViewSet):
#     queryset = Favorites.objects.all() # Update queryset to be a queryset
#     permission_classes = [permissions.IsAuthenticated]

#     def delete(self, request, *args, **kwargs):
#         favorite_id = kwargs.get('pk')
#         favorite = get_object_or_404(Favorites, id=favorite_id)

#         favorite.delete()

#         return Response(status=204)
