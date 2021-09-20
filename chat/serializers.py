from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.serializers import ModelSerializer, CharField, ReadOnlyField, SerializerMethodField

from chat.models import Message
from account.models import UserBase, Shop
from store.models import Product

class AccountModelSerializer(ModelSerializer):
    user_name = SerializerMethodField()
    
    class Meta:
        model = UserBase
        fields = ('uuid', 'user_name')
    
    def get_user_name(self, obj):
        return obj.user_name if hasattr(obj, 'shop') == False else "" 

class ShopModelSerializer(ModelSerializer):
    class Meta:
        model = Shop
        fields = ('title', 'image')

class ProductModelSerializer(ModelSerializer):
    absolute_url = ReadOnlyField(source='get_absolute_url')
    
    class Meta:
        model = Product
        fields = ('title', 'image', 'absolute_url')

class MessageModelSerializer(ModelSerializer):
    recipient = CharField(source='recipient.uuid')
    user = AccountModelSerializer(read_only=True)
    shop = ShopModelSerializer(source='user.shop', read_only=True)
    product = ProductModelSerializer(read_only=True)

    def create(self, validated_data):
        user = self.context['request'].user
        recipient = get_object_or_404(UserBase, uuid=validated_data['recipient']['uuid'])
        
        msg = Message(recipient=recipient, body=validated_data['body'], user=user)
        
        msg.save()
        
        return msg

    class Meta:
        model = Message
        fields = ('id', 'user', 'recipient', 'shop', 'product', 'created', 'body')


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('user_name',)
