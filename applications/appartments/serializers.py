from rest_framework import serializers
from .models import Appartment, Comment
 

class AppartmentListSerializer(serializers.ListSerializer):
    class Meta:
        model = Appartment
        fields = ('id', 'image', 'title', 'price')


class AppartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appartment
        fields = '__all__'
        read_only_fields = ['id', 'user']
        list_serializer_class = AppartmentListSerializer

    def create(self, validated_data):
        user = self.context.get('request').user
        validated_data['user'] = user
        return super().create(validated_data)
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['comments'] = CommentSerializer(instance.comments.all(), many=True).data
        return representation
    

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        fields = ('id', 'user', 'appartment', 'text', 'created_at', 'updated_at')
        read_only_fields = ['appartment']


# ПРОБНЫЙ ВАРИАНТ СЕРИАЛАЙЗЕРА

# class CommentSerializer(serializers.ModelSerializer):
#     user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

#     class Meta:
#         model = Comment
#         fields = (
#             'id', 'user', 'text', 'created_at', 
#             'updated_at', 'sub_comment', 'appartment'
#         )
#         read_only_fields = ['appartment']


'test'

# новый коммитаоо
